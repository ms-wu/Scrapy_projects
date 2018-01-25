import requests
import re
try:
    import cookielib  #python2
except:
    import http.cookiejar as cookielib  #python3

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookie.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie can't load")

agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-agent": agent
}

def is_login():
    #check the status is already login?
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True


def get_xsrf():
    #获取xrsf code
    response = session.get("https://www.zhihu.com", headers=header)
    match_obj = re.match('.*name="_xsrf" value="?(.*)"', response.text)
    if match_obj:
        return match_obj.group(1)
    else:
        return ""


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
        print("ok")

def zhihu_login(account, passwd):
    #知乎登录
    if re.match('^1\d{10}', account):
        print("login with phone number")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": passwd
        }
    else:
        if '@' in account:
            print("login with email")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": passwd
            }
    response_text = session.post(post_url, data=post_data, headers=header)
    session.cookies.save()


# zhihu_login("18782902568", "admin123")
get_index()