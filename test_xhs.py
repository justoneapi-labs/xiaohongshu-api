import io
import json
import unittest
from urllib.parse import parse_qs, urlparse
from urllib.error import HTTPError
from xhs import request

class ClientTests(unittest.TestCase):
    def test_search_encoding_and_pagination(self):
        def fake(url, timeout):
            u = urlparse(url)
            self.assertEqual(u.path, "/api/xiaohongshu/search-note/v4")
            self.assertEqual(parse_qs(u.query), {"token":["test-only"], "keyword":["咖啡 & 茶"], "page":["2"]})
            return io.StringIO(json.dumps({"code":0,"data":[]}))
        self.assertEqual(request("search","咖啡 & 茶","test-only",page=2,opener=fake)["data"],[])
    def test_missing_token_never_calls_network(self):
        def fail(*args, **kwargs):
            self.fail("Network must not be called")
        with self.assertRaises(ValueError):
            request("detail","id","",opener=fail)
    def test_http_error_does_not_expose_token(self):
        def fake(url, timeout):
            raise HTTPError(url,403,"test-only",None,None)
        with self.assertRaises(RuntimeError) as caught:
            request("detail","id","secret-test-token",opener=fake)
        self.assertNotIn("secret-test-token",str(caught.exception))
    def test_business_failure_is_not_success(self):
        with self.assertRaises(RuntimeError):
            request("comments","id","test-only",opener=lambda *a,**k:io.StringIO('{"code":402}'))
if __name__ == "__main__":
    unittest.main()
