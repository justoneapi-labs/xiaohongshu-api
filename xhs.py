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
}

def request(action, value, token, *, page=1, cursor="", opener=urlopen):
    if not token:
        raise ValueError("Set JUSTONEAPI_TOKEN before making a request.")
    path, key = ENDPOINTS[action]
    params = {"token": token, key: value}
    if action == "search":
        params["page"] = page
    if action == "comments" and cursor:
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
    parser.add_argument("value", help="Search keyword, or note ID for detail/comments")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--cursor", default="", help="Pass the cursor documented for the previous response")
    args = parser.parse_args()
    if args.page < 1:
        parser.error("--page must be at least 1")
    try:
        result = request(args.action, args.value, os.environ.get("JUSTONEAPI_TOKEN", ""), page=args.page, cursor=args.cursor)
    except (ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
