#!/usr/bin/env python3
"""
fetch_stats.py
Pulls public profile stats from the GitHub GraphQL API into assets/src/stats.json.
Token: GH_TOKEN / GITHUB_TOKEN, else `gh auth token`. On any failure the previous
stats.json is kept so the SVG build never breaks.
"""
import json, os, subprocess, sys, urllib.request

LOGIN = "OVERxPOWERED"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "src", "stats.json")
QUERY = """query($login:String!){user(login:$login){
 followers{totalCount} repositories(ownerAffiliations:OWNER,privacy:PUBLIC){totalCount}
 starred:repositories(ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false,first:100){nodes{stargazerCount languages(first:6,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}
 contributionsCollection{totalCommitContributions totalPullRequestContributions totalIssueContributions
  contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}}}}}"""

def token():
    t = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    return t or subprocess.check_output(["gh", "auth", "token"], text=True).strip()

OSS = ["NetPranav/Cero-Terminal", "NetPranav/WebGen"]

def rest(path):
    req = urllib.request.Request("https://api.github.com/" + path, headers={"Authorization": f"bearer {token()}"})
    return json.load(urllib.request.urlopen(req, timeout=20))

def oss():
    out = []
    for full in OSS:
        r = rest(f"repos/{full}")
        mine = next((c["contributions"] for c in rest(f"repos/{full}/contributors") if c["login"].lower() == LOGIN.lower()), 0)
        out.append({"repo": full, "name": r["name"], "desc": r["description"], "stars": r["stargazers_count"],
                    "pushed": r["pushed_at"][:10], "mine": mine, "topics": r.get("topics", [])})
    return out

def main():
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json"})
    u = json.load(urllib.request.urlopen(req, timeout=20))["data"]["user"]
    cc = u["contributionsCollection"]; days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    streak = 0
    for d in reversed(days):
        if d["contributionCount"] > 0: streak += 1
        elif d is days[-1]: continue          # today may still be empty
        else: break
    langs = {}
    for r in u["starred"]["nodes"]:
        for e in r["languages"]["edges"]: langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    tot = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
    stats = {"repos": u["repositories"]["totalCount"], "followers": u["followers"]["totalCount"],
             "stars": sum(r["stargazerCount"] for r in u["starred"]["nodes"]),
             "contributions": cc["contributionCalendar"]["totalContributions"], "commits": cc["totalCommitContributions"],
             "prs": cc["totalPullRequestContributions"], "issues": cc["totalIssueContributions"], "streak": streak,
             "langs": [[k, round(v * 100 / tot, 1)] for k, v in top],
             "days": [d["contributionCount"] for d in days]}
    try: stats["oss"] = oss()
    except Exception as e:
        print("oss fetch failed:", e, file=sys.stderr)
        if os.path.exists(OUT): stats["oss"] = json.load(open(OUT)).get("oss", [])
    json.dump(stats, open(OUT, "w"))
    print({k: v for k, v in stats.items() if k != "days"}, len(days), "days")

if __name__ == "__main__":
    try: main()
    except Exception as e:
        print("stats fetch failed, keeping cached stats.json:", e, file=sys.stderr)
        if not os.path.exists(OUT): sys.exit(1)
