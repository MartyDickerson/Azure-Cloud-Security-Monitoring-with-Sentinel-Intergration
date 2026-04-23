#!/usr/bin/env python3
import os
import sys
import argparse
import requests
from datetime import datetime, timezone

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID", "")
NOTION_API = "https://api.notion.com/v1"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def create_page(title, entry_type, description="", repo=None, url=None, tags=None):
    if not NOTION_TOKEN or not DATABASE_ID:
        print("Error: NOTION_TOKEN and NOTION_DATABASE_ID must be set.", file=sys.stderr)
        sys.exit(1)
    properties = {
        "Name": {"title": [{"text": {"content": title[:2000]}}]},
        "Type": {"select": {"name": entry_type}},
        "Date": {"date": {"start": datetime.now(timezone.utc).isoformat()}},
    }
    if description:
        properties["Description"] = {"rich_text": [{"text": {"content": description[:2000]}}]}
    if repo:
        properties["Repo"] = {"rich_text": [{"text": {"content": repo}}]}
    if url:
        properties["URL"] = {"url": url}
    if tags:
        properties["Tags"] = {"multi_select": [{"name": t.strip()} for t in tags if t.strip()]}
    response = requests.post(
        f"{NOTION_API}/pages", headers=HEADERS, json={"parent": {"database_id": DATABASE_ID}, "properties": properties}, timeout=10
    )
    if response.status_code != 200:
        print(f"Notion API error {response.status_code}: {response.text}", file=sys.stderr)
        response.raise_for_status()
    page = response.json()
    print(f"Logged [{entry_type}]: {title}")
    print(f"  -> {page.get('url', 'no URL returned')}")
    return page

def log_commit():
    message = os.environ.get("COMMIT_MESSAGE", "").strip()
    commit_url = os.environ.get("COMMIT_URL", "")
    repo = os.environ.get("REPO_NAME", "")
    branch = os.environ.get("BRANCH", "")
    author = os.environ.get("AUTHOR", "")
    if not message or message.startswith("Merge ") or "[skip notion]" in message:
        print("Skipping commit.")
        return
    repo_short = repo.split("/")[-1] if repo else repo
    title = f"[{repo_short}] {message[:120]}"
    description = "\n".join(filter(None, [f"Branch: {branch}", f"Author: {author}", "", message]))
    tags = ["Commit"] + ([repo_short] if repo_short else [])
    create_page(title, "Commit", description=description, repo=repo, url=commit_url, tags=tags)

def log_repo():
    repo = os.environ.get("REPO_NAME", "")
    repo_url = os.environ.get("REPO_URL", "")
    repo_desc = os.environ.get("REPO_DESC", "")
    repo_short = repo.split("/")[-1] if "/" in repo else repo
    create_page(f"New repo: {repo_short}", "Repo", description=repo_desc or f"New repository: {repo}", repo=repo, url=repo_url or None, tags=["New Repo", repo_short])

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("commit")
    sub.add_parser("repo")
    args = parser.parse_args()
    dispatch = {"commit": log_commit, "repo": log_repo}
    if args.command not in dispatch:
        parser.print_help()
        sys.exit(1)
    dispatch[args.command]()

if __name__ == "__main__":
    main()
