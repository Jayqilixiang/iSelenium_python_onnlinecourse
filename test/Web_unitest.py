import allure
import configparser
import os
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


@allure.feature('Test Baidu WebUI')
class ISelenium(unittest.TestCase):
    # 读取配置文件
    def get_config(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.environ['HOME'], 'iselenium.ini'))
        return config

    # 清理缓存
    def tearDown(self):
        self.driver.quit()

    def setUp(self):
        config = self.get_config()

        # 控制是否采用无界面形式运行自动化测试
        try:
            using_headless = os.environ["using_headless"]
        # 防止没有配置环境变量而导致出错，headless是用无界面运行，需要配置环境变量
        except KeyError:
            using_headless = None
            print('没有配置环境变量 using_headless, 按照有界面方式运行自动化测试')

        chrome_options = Options()
        if using_headless is not None and using_headless.lower() == 'true':
            print('使用无界面方式运行')
            chrome_options.add_argument("--headless")
        # 实例化 chromedriver
        self.driver = webdriver.Chrome(executable_path=config.get('driver', 'chrome_driver'), # 读取配置文件ini中的driver
                                       options=chrome_options)

    @allure.story('Test key word 今日头条')
    def test_webui_1(self):
        """ 测试用例1，验证'今日头条'关键词在百度上的搜索结果
        """
        # 封装到下面的方法
        self._test_baidu('今日头条', 'test_webui_1')

    @allure.story('Test key word 王者荣耀')
    def test_webui_2(self):
        """ 测试用例2， 验证'王者荣耀'关键词在百度上的搜索结果
        """

        self._test_baidu('王者荣耀', 'test_webui_2')

    def _test_baidu(self, search_keyword, testcase_name):
        """ 测试百度搜索子函数

        :param search_keyword: 搜索关键词 (str)
        :param testcase_name: 测试用例名 (str)
        """

        self.driver.get("https://www.baidu.com")
        print('打开浏览器，访问 www.baidu.com .')
        time.sleep(5)
        # 验证标题
        assert f'百度一下' in self.driver.title

        # by_name定位元素
        elem = self.driver.find_element_by_name("wd")
        elem.send_keys(f'{search_keyword}{Keys.RETURN}') # 在搜索框输入查找词后，键盘回车 操作
        print(f'搜索关键词~{search_keyword}')
        time.sleep(5)
        self.assertTrue(f'{search_keyword}' in self.driver.title, msg=f'{testcase_name}校验点 pass')
