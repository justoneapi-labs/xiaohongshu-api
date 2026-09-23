"""Small Xiaohongshu API client. Uses Python standard library only."""
import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

ENDPOINTS = {
    "search": ("/api/xiaohongshu/search-note/v4", "keyword"),
    "detail": ("/api/xiaohongshu/get-note-detail/v6", "noteId"),
    "comments": ("/api/xiaohongshu/get-note-comment/v4", "noteId"),
    "replies": ("/api/xiaohongshu/get-note-sub-comment/v2", "noteId"),
}

def request(action, value, token, *, page=1, cursor="", comment_id="", opener=urlopen):
    if not token:
        raise ValueError("Set JUSTONEAPI_TOKEN before making a request.")
    if action == "replies" and not comment_id:
        raise ValueError("Set --comment-id to the parent comment ID for replies.")
    path, key = ENDPOINTS[action]
    params = {"token": token, key: value}
    if action == "search":
        params["page"] = page
    if action == "replies":
        params["commentId"] = comment_id
    if action in ("comments", "replies") and cursor:
        params["lastCursor"] = cursor
    url = "https://api.justoneapi.com" + path + "?" + urlencode(params)
    try:
        with opener(url, timeout=30) as response:
            result = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}; check account and endpoint documentation.") from None
    except (URLError, TimeoutError):
        raise RuntimeError("Network request failed; retry manually after checking connectivity.") from None
    except (ValueError, UnicodeError):
        raise RuntimeError("Server returned invalid JSON.") from None
    if not isinstance(result, dict) or result.get("code") != 0:
        code = result.get("code") if isinstance(result, dict) else None
        raise RuntimeError(f"API request failed (code={code}). Check the API documentation.")
    return result

def main():
    parser = argparse.ArgumentParser(description="小红书API / 小红书接口 — Just One API examples")
    parser.add_argument("action", choices=ENDPOINTS)
    parser.add_argument("value", help="Search keyword, or note ID for detail/comments/replies")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--cursor", default="", help="Pass the cursor documented for the previous response")
    parser.add_argument("--comment-id", default="", help="Parent comment ID (required for replies)")
    args = parser.parse_args()
    if args.page < 1:
        parser.error("--page must be at least 1")
    if args.action == "replies" and not args.comment_id:
        parser.error("--comment-id is required for replies")
    try:
        result = request(args.action, args.value, os.environ.get("JUSTONEAPI_TOKEN", ""), page=args.page, cursor=args.cursor, comment_id=args.comment_id)
    except (ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
