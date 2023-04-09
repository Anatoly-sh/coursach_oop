import re


def clean_text(param: str, param1: str) -> str:
    return re.sub(param, "", param1)
