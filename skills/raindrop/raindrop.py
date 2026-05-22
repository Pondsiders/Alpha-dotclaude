#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Raindrop.io API client for managing Jeffery's bookmarks.

Usage:
    raindrop.py collections                     # List all collections
    raindrop.py list [COLLECTION]               # List bookmarks (default: Unsorted)
    raindrop.py browse [TAG]                    # List bookmarks WITHOUT the tag (default: 🦆)
    raindrop.py search QUERY                    # Search all bookmarks
    raindrop.py get ID                          # Get single bookmark details
    raindrop.py tags                            # List all tags
    raindrop.py add URL [--collection C] [--tags t1,t2] [--title T]
    raindrop.py update ID [--tags t1,t2] [--collection C] [--title T]
    raindrop.py move ID COLLECTION              # Move bookmark to collection
    raindrop.py tag ID TAG [TAG...]             # Add tags (preserves existing)
    raindrop.py done ID                         # Move to Archive, add "read" tag

Environment:
    RAINDROP_TOKEN — API test token (required)
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://api.raindrop.io/rest/v1"


def get_token() -> str:
    """Read the Raindrop API token from the environment."""
    token = os.environ.get("RAINDROP_TOKEN")
    if not token:
        print("Error: RAINDROP_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)
    return token


def api_request(method: str, endpoint: str, data: dict | None = None) -> dict:
    """Make an API request to Raindrop and return the parsed JSON body."""
    url = f"{BASE_URL}/{endpoint}"
    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"API Error {e.code}: {e.reason}", file=sys.stderr)
        if error_body:
            print(error_body, file=sys.stderr)
        sys.exit(1)


def get_collections() -> dict:
    """Get all collections, returns a {name|id: id} lookup map."""
    result = api_request("GET", "collections")
    collections = {}
    for item in result.get("items", []):
        collections[item["title"].lower()] = item["_id"]
        collections[str(item["_id"])] = item["_id"]
    return collections


def resolve_collection(name_or_id: str) -> int:
    """Resolve a collection name or numeric ID to its integer ID."""
    collections = get_collections()
    key = name_or_id.lower() if isinstance(name_or_id, str) else str(name_or_id)
    if key in collections:
        return collections[key]
    try:
        return int(name_or_id)
    except ValueError:
        print(f"Error: Unknown collection '{name_or_id}'", file=sys.stderr)
        print(f"Available: {', '.join(c for c in collections if not c.isdigit())}", file=sys.stderr)
        sys.exit(1)


def cmd_collections() -> None:
    """List all collections."""
    result = api_request("GET", "collections")
    print("# Collections\n")
    for item in sorted(result.get("items", []), key=lambda x: x["title"]):
        count = item.get("count", 0)
        print(f"- **{item['title']}** ({count} items) — ID: {item['_id']}")


def cmd_list(collection: str = "-1", limit: int = 25) -> None:
    """List bookmarks in a collection. Default: Unsorted (-1). Use 0 for All."""
    collection_id = int(collection) if collection in ("-1", "0") else resolve_collection(collection)
    result = api_request("GET", f"raindrops/{collection_id}?perpage={limit}")

    total = result.get("count", "?")

    if collection_id == -1:
        coll_name = "Unsorted"
    elif collection_id == 0:
        coll_name = "All Bookmarks"
    else:
        collections = api_request("GET", "collections")
        coll_name = collection
        for c in collections.get("items", []):
            if c["_id"] == collection_id:
                coll_name = c["title"]
                break

    items = result.get("items", [])
    print(f"# {coll_name} ({len(items)} of {total})\n")

    for item in items:
        tags = ", ".join(item.get("tags", [])) if item.get("tags") else ""
        tag_str = f" [{tags}]" if tags else ""
        print(f"- **{item['title']}**{tag_str}")
        print(f"  ID: {item['_id']} | {item['link']}")
        if item.get("excerpt"):
            excerpt = item["excerpt"][:150] + "..." if len(item.get("excerpt", "")) > 150 else item.get("excerpt", "")
            print(f"  _{excerpt}_")
        print()


def cmd_search(query: str, limit: int = 20) -> None:
    """Search all bookmarks."""
    params = urllib.parse.urlencode({"search": query, "perpage": limit})
    result = api_request("GET", f"raindrops/0?{params}")

    items = result.get("items", [])
    print(f"# Search: '{query}' ({len(items)} results)\n")

    for item in items:
        tags = ", ".join(item.get("tags", [])) if item.get("tags") else ""
        tag_str = f" [{tags}]" if tags else ""
        print(f"- **{item['title']}**{tag_str}")
        print(f"  ID: {item['_id']} | {item['link']}")
        if item.get("excerpt"):
            excerpt = item["excerpt"][:150] + "..." if len(item.get("excerpt", "")) > 150 else item.get("excerpt", "")
            print(f"  _{excerpt}_")
        print()


def cmd_browse(exclude_tag: str = "🦆", compact: bool = True) -> None:
    """Browse all bookmarks that DON'T have a given tag. Paginated across all pages."""
    page = 0
    all_items = []
    while True:
        search = urllib.parse.quote(f"-#{exclude_tag}")
        result = api_request("GET", f"raindrops/0?search={search}&perpage=50&page={page}")
        items = result.get("items", [])
        if not items:
            break
        all_items.extend(items)
        page += 1

    print(f"# Unread ({len(all_items)} bookmarks without #{exclude_tag})\n")

    for item in all_items:
        tags = item.get("tags", [])
        tag_str = f" [{', '.join(tags)}]" if tags else ""
        if compact:
            print(f"- {item['title']}{tag_str} (ID: {item['_id']})")
        else:
            print(f"- **{item['title']}**{tag_str}")
            print(f"  ID: {item['_id']} | {item['link']}")
            if item.get("excerpt"):
                excerpt = item["excerpt"][:150] + "..." if len(item.get("excerpt", "")) > 150 else item.get("excerpt", "")
                print(f"  _{excerpt}_")
            print()


def cmd_get(raindrop_id: int) -> None:
    """Get details for a single bookmark."""
    result = api_request("GET", f"raindrop/{raindrop_id}")
    item = result.get("item", {})

    print(f"# {item.get('title', 'Untitled')}\n")
    print(f"**URL:** {item.get('link', 'N/A')}")
    print(f"**ID:** {item.get('_id')}")
    print(f"**Type:** {item.get('type', 'N/A')}")
    print(f"**Tags:** {', '.join(item.get('tags', [])) or 'None'}")
    print(f"**Created:** {item.get('created', 'N/A')}")

    if item.get("excerpt"):
        print(f"\n**Excerpt:**\n{item['excerpt']}")

    if item.get("note"):
        print(f"\n**Notes:**\n{item['note']}")


def cmd_tags() -> None:
    """List all tags."""
    result = api_request("GET", "tags")
    print("# Tags\n")
    for tag in sorted(result.get("items", []), key=lambda x: -x.get("count", 0)):
        print(f"- {tag['_id']} ({tag.get('count', 0)})")


def cmd_add(url: str, collection: str | None = None, tags: list | None = None, title: str | None = None) -> None:
    """Add a new bookmark."""
    data: dict = {"link": url}

    if collection:
        data["collection"] = {"$id": resolve_collection(collection)}
    if tags:
        data["tags"] = tags
    if title:
        data["title"] = title

    result = api_request("POST", "raindrop", data)
    item = result.get("item", {})
    print(f"✓ Added: **{item.get('title', url)}**")
    print(f"  ID: {item.get('_id')} | Collection: {item.get('collection', {}).get('$id', 'Unsorted')}")


def cmd_update(raindrop_id: int, tags: list | None = None, collection: str | None = None, title: str | None = None) -> None:
    """Update an existing bookmark."""
    data: dict = {}
    if tags is not None:
        data["tags"] = tags
    if collection:
        data["collection"] = {"$id": resolve_collection(collection)}
    if title:
        data["title"] = title

    if not data:
        print("Nothing to update", file=sys.stderr)
        return

    result = api_request("PUT", f"raindrop/{raindrop_id}", data)
    item = result.get("item", {})
    print(f"✓ Updated: **{item.get('title')}**")


def cmd_move(raindrop_id: int, collection: str) -> None:
    """Move bookmark to a collection."""
    collection_id = resolve_collection(collection)
    data = {"collection": {"$id": collection_id}}
    result = api_request("PUT", f"raindrop/{raindrop_id}", data)
    item = result.get("item", {})
    print(f"✓ Moved '{item.get('title')}' to collection {collection}")


def cmd_tag(raindrop_id: int, new_tags: list) -> None:
    """Add tags to a bookmark (preserving existing)."""
    result = api_request("GET", f"raindrop/{raindrop_id}")
    current_tags = result.get("item", {}).get("tags", [])

    all_tags = list(set(current_tags + new_tags))

    result = api_request("PUT", f"raindrop/{raindrop_id}", {"tags": all_tags})
    item = result.get("item", {})
    print(f"✓ Tagged '{item.get('title')}': {', '.join(all_tags)}")


def cmd_done(raindrop_id: int) -> None:
    """Mark as read: move to Archive and add 'read' tag."""
    result = api_request("GET", f"raindrop/{raindrop_id}")
    item = result.get("item", {})
    current_tags = item.get("tags", [])

    archive_id = resolve_collection("archive")

    new_tags = list(set(current_tags + ["read"]))
    data = {
        "tags": new_tags,
        "collection": {"$id": archive_id},
    }

    result = api_request("PUT", f"raindrop/{raindrop_id}", data)
    updated = result.get("item", {})
    print(f"✓ Done: '{updated.get('title')}'")
    print("  Moved to Archive, tagged 'read'")


def main() -> None:
    """Dispatch a subcommand from sys.argv."""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
        return

    cmd = args[0].lower()

    if cmd == "collections":
        cmd_collections()

    elif cmd == "list":
        collection = "-1"
        limit = 25
        i = 1
        while i < len(args):
            if args[i] == "--limit" and i + 1 < len(args):
                limit = int(args[i + 1])
                i += 2
            elif not args[i].startswith("--"):
                collection = args[i]
                i += 1
            else:
                i += 1
        cmd_list(collection, limit)

    elif cmd == "browse":
        exclude = args[1] if len(args) > 1 and not args[1].startswith("--") else "🦆"
        verbose = "--verbose" in args or "-v" in args
        cmd_browse(exclude_tag=exclude, compact=not verbose)

    elif cmd == "search":
        if len(args) < 2:
            print("Usage: raindrop.py search QUERY", file=sys.stderr)
            sys.exit(1)
        cmd_search(" ".join(args[1:]))

    elif cmd == "get":
        if len(args) < 2:
            print("Usage: raindrop.py get ID", file=sys.stderr)
            sys.exit(1)
        cmd_get(int(args[1]))

    elif cmd == "tags":
        cmd_tags()

    elif cmd == "add":
        if len(args) < 2:
            print("Usage: raindrop.py add URL [--collection C] [--tags t1,t2]", file=sys.stderr)
            sys.exit(1)
        url = args[1]
        collection = None
        tags = None
        title = None
        i = 2
        while i < len(args):
            if args[i] == "--collection" and i + 1 < len(args):
                collection = args[i + 1]
                i += 2
            elif args[i] == "--tags" and i + 1 < len(args):
                tags = args[i + 1].split(",")
                i += 2
            elif args[i] == "--title" and i + 1 < len(args):
                title = args[i + 1]
                i += 2
            else:
                i += 1
        cmd_add(url, collection, tags, title)

    elif cmd == "update":
        if len(args) < 2:
            print("Usage: raindrop.py update ID [--tags t1,t2] [--collection C]", file=sys.stderr)
            sys.exit(1)
        raindrop_id = int(args[1])
        tags = None
        collection = None
        title = None
        i = 2
        while i < len(args):
            if args[i] == "--collection" and i + 1 < len(args):
                collection = args[i + 1]
                i += 2
            elif args[i] == "--tags" and i + 1 < len(args):
                tags = args[i + 1].split(",")
                i += 2
            elif args[i] == "--title" and i + 1 < len(args):
                title = args[i + 1]
                i += 2
            else:
                i += 1
        cmd_update(raindrop_id, tags, collection, title)

    elif cmd == "move":
        if len(args) < 3:
            print("Usage: raindrop.py move ID COLLECTION", file=sys.stderr)
            sys.exit(1)
        cmd_move(int(args[1]), args[2])

    elif cmd == "tag":
        if len(args) < 3:
            print("Usage: raindrop.py tag ID TAG [TAG...]", file=sys.stderr)
            sys.exit(1)
        cmd_tag(int(args[1]), args[2:])

    elif cmd == "done":
        if len(args) < 2:
            print("Usage: raindrop.py done ID", file=sys.stderr)
            sys.exit(1)
        cmd_done(int(args[1]))

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print("Try: collections, list, browse, search, get, tags, add, update, move, tag, done", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
