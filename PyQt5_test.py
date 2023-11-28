from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
driver.get('https://www.douban.com/')
time.sleep(1)
iframe = self.driver.find_element(By.TAG_NAME, 'iframe') # 主代码在iframe里面，要先切进去
driver.switch_to.frame(iframe)  # 切到内层
time.sleep(0.5)
# 模拟点击切换  至账号密码登录界面
driver.find_element(By.CLASS_NAME, 'account-tab-account').click()
time.sleep(0.1)
driver.find_element(By.ID, 'username').send_keys('19******25')  # 模拟键盘输入账号
time.sleep(0.2)
driver.find_element(By.ID, 'password').send_keys('*********')  # 模拟键盘输入密码
driver.find_element(By.CSS_SELECTOR, '.btn-account').click()  # 点击登录按钮
# 输出登陆之后的cookies
print(self.driver.get_cookies())
time.sleep(0.1)
# 截图保存登陆成功界面
driver.save_screenshot("reimgs/douban.jpg")