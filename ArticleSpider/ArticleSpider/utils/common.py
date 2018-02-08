import hashlib
import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
    # 从字符串中提取数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        value = int(match_re.group(1))
    else:
        value = 0
    return value