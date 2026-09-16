# Xiaohongshu API examples

Minimal Python examples for Xiaohongshu note search, note details and comments through Just One API. [简体中文](README.md)

This is a third-party service integration, not an official Xiaohongshu SDK. Source code is MIT-licensed; API access requires a Just One API token and may incur charges. See the dashboard for pricing and permissions.

## Quick start

Python 3.10+, no third-party dependencies:

```bash
git clone https://github.com/justoneapi-labs/justoneapi-xiaohongshu-api.git
cd justoneapi-xiaohongshu-api
export JUSTONEAPI_TOKEN='YOUR_TOKEN'
python xhs.py search 'coffee' --page 1
python xhs.py detail 'YOUR_NOTE_ID'
python xhs.py comments 'YOUR_NOTE_ID'
```

Each invocation sends one request. No automatic bulk pagination or retries. For comments, use `--cursor` with the cursor documented for the previous response. Tokens are query parameters read from the environment. Never commit credentials.

Successful responses (`code == 0`) are printed as JSON. HTTP, network and business errors produce a nonzero exit code without printing the request URL. Response data varies by endpoint/version; consult the [API documentation](https://docs.justoneapi.com/en/?utm_source=github.com&utm_medium=referral&utm_campaign=justoneapi_labs_justoneapi_xiaohongshu_api&utm_content=readme_docs).

## Endpoints

- Search: `GET /api/xiaohongshu/search-note/v4`, `keyword`, optional `page`.
- Details: `GET /api/xiaohongshu/get-note-detail/v6`, `noteId`.
- Comments: `GET /api/xiaohongshu/get-note-comment/v4`, `noteId`, optional `lastCursor`.

All requests use `https://api.justoneapi.com` and a `token` query parameter.

## Tests

Run `python -m unittest -v`. Tests mock the network and do not make paid API calls or establish live endpoint health.

[Get a token](https://dashboard.justoneapi.com/en/login?utm_source=github.com&utm_medium=referral&utm_campaign=justoneapi_labs_justoneapi_xiaohongshu_api&utm_content=readme_token) · [Website](https://justoneapi.com/en/?utm_source=github.com&utm_medium=referral&utm_campaign=justoneapi_labs_justoneapi_xiaohongshu_api&utm_content=readme_home) · [Full Python SDK](https://github.com/justoneapi-labs/justoneapi-python)
