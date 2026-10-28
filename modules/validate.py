import re
import ipaddress

_DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$", re.I
)

def is_valid_target(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return bool(_DOMAIN_RE.match(target))
