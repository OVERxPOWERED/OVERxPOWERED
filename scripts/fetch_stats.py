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

PROFILE_REPO = LOGIN.lower()
ACTIVITY = """query($login:String!){user(login:$login){contributionsCollection{
 commitContributionsByRepository(maxRepositories:100){repository{nameWithOwner owner{login}} contributions(first:1,orderBy:{field:OCCURRED_AT,direction:DESC}){totalCount nodes{occurredAt}}}
 pullRequestContributionsByRepository(maxRepositories:100){repository{nameWithOwner owner{login}} contributions(first:1,orderBy:{direction:DESC}){totalCount nodes{occurredAt}}}}}}"""

def rest(path):
    req = urllib.request.Request("https://api.github.com/" + path, headers={"Authorization": f"bearer {token()}"})
    return json.load(urllib.request.urlopen(req, timeout=20))

def gql(query):
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=20))["data"]["user"]

def card(full, r, mine=0, active=None):
    try: langs = list(rest(f"repos/{full}/languages"))[:3]
    except Exception: langs = [r["language"]] if r.get("language") else []
    return {"repo": full, "name": r["name"], "desc": r["description"] or "", "stars": r["stargazers_count"],
            "pushed": (active or r["pushed_at"])[:10], "mine": mine, "langs": langs, "topics": r.get("topics", [])[:3]}

def recent_work(n=4):
    """Own repos (forks included, profile repo excluded), newest push first."""
    repos = rest(f"users/{LOGIN}/repos?sort=pushed&direction=desc&per_page=30&type=owner")
    repos = [r for r in repos if r["name"].lower() != PROFILE_REPO and not r["archived"]]
    return [card(r["full_name"], r, active=r["pushed_at"]) for r in repos[:n]]

def recent_oss(n=4):
    """Repos owned by others that I committed to or opened PRs against, most recent activity first."""
    cc = gql(ACTIVITY)["contributionsCollection"]; last = {}; mine = {}
    for kind in ("commitContributionsByRepository", "pullRequestContributionsByRepository"):
        for e in cc[kind]:
            repo = e["repository"]
            if repo["owner"]["login"].lower() == LOGIN.lower() or not e["contributions"]["nodes"]: continue
            full = repo["nameWithOwner"]; t = e["contributions"]["nodes"][0]["occurredAt"]
            last[full] = max(last.get(full, ""), t)
            if kind.startswith("commit"): mine[full] = e["contributions"]["totalCount"]
    return [card(f, rest(f"repos/{f}"), mine.get(f, 0), last[f]) for f in sorted(last, key=last.get, reverse=True)[:n]]

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
    for key, fn in (("work", recent_work), ("oss", recent_oss)):
        try: stats[key] = fn()
        except Exception as e:
            print(key, "fetch failed:", e, file=sys.stderr)
            if os.path.exists(OUT): stats[key] = json.load(open(OUT)).get(key, [])
    json.dump(stats, open(OUT, "w"))
    print({k: v for k, v in stats.items() if k != "days"}, len(days), "days")

if __name__ == "__main__":
    try: main()
    except Exception as e:
        print("stats fetch failed, keeping cached stats.json:", e, file=sys.stderr)
        if not os.path.exists(OUT): sys.exit(1)
