import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import subprocess
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


def read_config():
    """"读取配置"""
    with open("config.json") as json_file:
        config = json.load(json_file)
    return config


def load_driver(config):
    # 驱动程序
    # driver = webdriver.Chrome()
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    service = ChromeService(executable_path=config["chrome_drive_path"])
    options = ChromeOptions()
    # 无头模式
    if config["head_less"]:
        options.add_argument("--headless=new")
    if config["ignore_ssl"]:
        options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(service=service, options=options)
    return driver


class Spider:
    def __init__(self, config, driver):
        self.config = config
        self.driver = driver

    def spider(self):
        print("\n====================")
        web_login_url = self.config["web_login_url"]
        if web_login_url == "":
            web_login_url = "http://lab-net-test.connect.huxiaofan.com/"
        # 使用跳转防止出现nas问题
        self.driver.get(web_login_url)
        # driver.get('http://lab-net-test.connect.huxiaofan.com/')  # 这里输入你的校园网登录网址
        # driver.get('https://login.hdu.edu.cn/srun_portal_pc')  # 这里输入你的校园网登录网址
        time.sleep(3)

        # 获取当前 域名
        # 执行 JavaScript 获取域名
        domain = self.driver.execute_script("return window.location.hostname")
        print("检测域名为：", domain)

        if domain == "myip.ipip.net":
            print("已跳转到ip检测页，有网")
            # 获取整个页面的 HTML 内容
            # 获取接口返回的文本内容
            response_text = self.driver.find_element(By.TAG_NAME, "pre").text
            print(response_text)
        else:
            print("似乎没网，准备进行认证")
            username = self.config["username"]
            # 用户名
            # <input type="text" id="username" class="input-box" placeholder="学/工号">
            input_tag_username = self.driver.find_element(By.XPATH,
                                                          "//input[@id='username' and @class='input-box']")  # 通过xpath确定账号框位置
            input_tag_username.send_keys(username)  # 输入账号
            print("用户名自动填写成功")

            password = self.config["password"]
            # 密码
            # <input type="password" id="password" class="input-box" placeholder="密码">
            input_tag_password = self.driver.find_element(By.XPATH,
                                                          "//input[@id='password' and @class='input-box']")  # 通过xpath确定密码框位置
            input_tag_password.send_keys(password)  # 输入密码
            print("密码自动填写成功")

            # 进行登录(回车法)
            # input_tag_password.send_keys(Keys.ENTER)  # 敲一下回车

            # 按钮法
            # <button type="button" class="btn-login" id="login-account">
            login_button = self.driver.find_element(By.XPATH,
                                                    "//button[@class='btn-login' and @id='login-account']")  # 找到开通网络按钮
            login_button.click()
            print("连接网络中·····")
            time.sleep(2)
            print("登录成功")
        print("====================\n")


# 测试网络是否连通
def Ping():
    backinfo = subprocess.call('ping www.baidu.com -n 1', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    if backinfo:
        print('ping检测网络未连接')
        return 1
    else:
        print("ping检测有网")
        return 2


if __name__ == '__main__':
    print("HDU校园网自动守护脚本 by xiaofan")
    config = read_config()
    driver = load_driver(config)
    spider = Spider(config, driver)
    # 实例化对象
    while True:
        try:
            spider.spider()
            connection = Ping()
            if connection == 2:
                print("--> 网络正常，继续守护")
                time.sleep(config["check_interval"])
            elif connection == 1:
                print("-->网络异常，准备重新连接")
        except Exception as e:
            print("Oh damn --- 出错了")
            print(e)
            time.sleep(60)
