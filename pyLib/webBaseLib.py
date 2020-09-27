
from selenium import webdriver
from time import sleep
from cfg import g_login_url

class WebBaseLib:

    driver = None

    """写为类方法，才保证其他文件调用的是同一个驱动"""
    @classmethod
    def open_browser(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)

    """也可下面方法写"""
    # def open_browser(self):
    #     WebBaseLib.driver = webdriver.Chrome()
    #     self.driver.implicitly_wait(5)

    def close_browser(self):
        self.driver.quit()

    def user_login(self,username,password,isStudent=True):
        """
        用户登录
        :param isStudent: 如果是老师，需要带值False
        :return:
        """
        self.driver.get(g_login_url)
        if isStudent:    # 如果是学生，点击“学生登录”
            self.driver.find_element_by_css_selector('.student a').click()
        else:            # 否则，点击老师登录
            self.driver.find_element_by_css_selector('.teacher a').click()
        # 登录名框输入用户名
        sleep(1)
        input_username = self.driver.find_element_by_id('username')
        input_username.clear()
        input_username.send_keys(username)
        # 密码框输入密码
        input_password = self.driver.find_element_by_id('password')
        input_password.clear()
        input_password.send_keys(password)
        sleep(3)
        # 点击“登录”
        self.driver.find_element_by_id('submit').click()
        # 检查登录成功(成功后页面的某个元素存在)
        self.driver.find_element_by_css_selector(".img-responsive")  # 这里是头像图片


if __name__ == '__main__':
    obj=WebBaseLib()
    # obj.open_browser()

