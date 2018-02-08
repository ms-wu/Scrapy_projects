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
    response_text = response.text
    print(response.text)
    match_obj = re.match('.*srf&quot;:&quot;(.*?)&quot;,', response_text, re.DOTALL)
    print(match_obj.group(1))
    if match_obj:
        return match_obj.group(1)
    else:
        return ""


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index.html", "wb") as f:
        f.write(response.text.encode('utf-8'))
        print("ok")

def get_captcha():
    import time
    t = str(int(time.time()*1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t = session.get(captcha_url, headers=header)
    with open("captcha.jpg","wb") as f:
        f.write(t.content)
        f.close()

    from PIL import Image
    try:
        im = Image.open("captcha.jpg")
        im.show()
        im.close()
    except:
        pass
    captcha = input("输入验证码\n>")
    return captcha

def zhihu_login(account, passwd):
    #知乎登录
    if re.match('^1\d{10}', account):
        print("login with phone number")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": passwd,
            "captcha": get_captcha()
        }
    else:
        if '@' in account:
            print("login with email")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": passwd,
                "captcha": get_captcha()
            }
    response_text = session.post(post_url, data=post_data, headers=header)
    session.cookies.save()


zhihu_login("", "")
# get_index()
is_login()
# get_captcha()