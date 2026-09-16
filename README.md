# 小红书API · 小红书接口

使用 Just One API 调用小红书笔记搜索、笔记详情和评论接口。提供可以直接运行的 Python 示例，无第三方 Python 依赖。

[English](README.en.md) · [接口文档](https://docs.justoneapi.com/zh/?utm_source=github.com&utm_medium=referral&utm_campaign=justoneapi_labs_xiaohongshu_api&utm_content=readme_docs) · [获取 Token](https://dashboard.justoneapi.com/zh/login?utm_source=github.com&utm_medium=referral&utm_campaign=justoneapi_labs_xiaohongshu_api&utm_content=readme_token)

这是 **Just One API 第三方服务的调用示例**，不是小红书官方 SDK。示例代码开源，接口服务需要 Just One API Token，调用费用及可用性以控制台和在线文档为准。

## 三分钟开始

需要 Python 3.10 或更高版本。

```bash
git clone https://github.com/justoneapi-labs/xiaohongshu-api.git
cd xiaohongshu-api
export JUSTONEAPI_TOKEN='替换成你自己的 Token'
python xhs.py search '咖啡'
```

每次命令发出一个请求，不会自动遍历全部结果或重试。不要把真实 Token 提交进 Git。

## 小红书接口示例

| 功能 | GET 接口 | 必填业务参数 |
|---|---|---|
| 笔记搜索 | `/api/xiaohongshu/search-note/v4` | `keyword` |
| 笔记详情 | `/api/xiaohongshu/get-note-detail/v6` | `noteId` |
| 笔记评论 | `/api/xiaohongshu/get-note-comment/v4` | `noteId` |

所有请求额外携带 `token` 查询参数，示例从环境变量读取。接口路径和参数基于公开 OpenAPI；完整过滤参数、返回字段和版本状态以在线文档为准。

```bash
# 搜索第二页
python xhs.py search '咖啡' --page 2

# 查看一篇笔记：将示例占位符替换为真实笔记 ID
python xhs.py detail 'YOUR_NOTE_ID'

# 获取评论第一页
python xhs.py comments 'YOUR_NOTE_ID'

# 获取后续评论：按文档从上一次响应提取游标
python xhs.py comments 'YOUR_NOTE_ID' --cursor 'PREVIOUS_CURSOR'
```

## 返回结果与错误

成功时输出服务端完整 JSON，`code == 0` 才视为成功。`data` 的具体结构取决于接口版本；本示例不假设笔记列表或游标位于固定字段。

未设置 Token、HTTP 错误、网络错误或业务失败时，以非零退出码结束。错误信息不打印包含 Token 的请求 URL。遇到接口失败时先查看账户余额、权限及在线文档，不要循环重试。

## 用于你的项目

```python
import os
from xhs import request

result = request('search', '咖啡', os.environ['JUSTONEAPI_TOKEN'])
print(result['data'])
```

需要异步客户端和更多平台时，可以使用 [Just One API Python SDK](https://github.com/justoneapi-labs/justoneapi-python)。本仓库专注于小红书API的最小调用流程。

## 测试

```bash
python -m unittest -v
```

测试使用模拟响应，不调用付费接口；这些测试不代表线上接口健康状态。

## 文档与支持

- [Just One API 官网](https://justoneapi.com/zh/?utm_source=github.com&utm_medium=referral&utm_campaign=justoneapi_labs_xiaohongshu_api&utm_content=readme_home)
- [小红书接口及其他接口文档](https://docs.justoneapi.com/zh/?utm_source=github.com&utm_medium=referral&utm_campaign=justoneapi_labs_xiaohongshu_api&utm_content=readme_docs)
- 示例代码问题可以提交本仓库 Issue；请移除 Token 和私人数据。

## 许可证

示例代码采用 MIT License，API 服务使用条款独立于代码许可证。
