from selenium import webdriver
from scrapy.selector import Selector
import time

chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_opt.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(executable_path="H:\chromedriver.exe", chrome_options=chrome_opt)
browser.get("https://www.taobao.com")
# time.sleep(5)

# browser.find_element_by_css_selector()
# t_selector = Selector(text=browser.page_source)
# t_selector.css()

# for i in range(3):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
#     time.sleep(3)



# browser.quit()