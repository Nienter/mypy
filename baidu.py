from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
cookie1 = {"name": "BAIDUID", "value": "10E914E5D9CAF4E46F5A6058D33C2B72:FG=1"}

cookie2 = {"name": "BDUSS",
           "value": "xsMTllYX5lWlZxemFtby1MZU02Z3EyOGtBWjhPWDFWNk1Jb0RzZ2hDc28zNzFnRVFBQUFBJCQAAAAAAAAAAAEAAAAibfIM0"
                    "-7DztH0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAChSlmAoUpZgOE"}
time.sleep(5)
driver.add_cookie(cookie1)
driver.add_cookie(cookie2)
driver.get("https://www.baidu.com")
print(driver.get_cookies())
