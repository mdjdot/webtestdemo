#!/usr/bin/env python3
import pytest
from selenium import webdriver
import uiautomation as uia
import time
import sys
import os
import configparser
from PIL import Image
import math
import operator
from functools import reduce


def test_search_img():
    currentPath = os.path.abspath(
        os.path.dirname(__file__))
    config = configparser.ConfigParser()
    config.read(os.path.join(currentPath, 'config.ini'))

    # 1. start Chrome and set to maximized
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    driver.maximize_window()
    driver.implicitly_wait(10)

    # 2. goto 'https://www.baidu.com/'
    # driver.get('https://www.google.com/imghp?hl=zh-CN&tab=wi&ogbl')
    driver.get('https://www.baidu.com/')
    driver.find_element_by_class_name('soutu-btn').click()
    time.sleep(5)

    # 3. upload an image and start searching
    uia.ButtonControl(Name='选择文件').Click()
    window = uia.WindowControl(ClassName='#32770')
    filePath = os.path.join(currentPath, 'pythontab.jpg')
    uia.SendKeys(filePath)
    uia.ButtonControl(AutomationId='1').Click()
    time.sleep(10)
    driver.save_screenshot('1.png')

    # 4. get the target search result and validate it
    target = int(config.get('CheckPoint', 'VISIT_RESULT'))
    img = driver.find_element_by_css_selector(
        'div.graph-row.graph-same-list > div:nth-child(3) > div > a > div.graph-same-list-img > img')
    img.screenshot('./tempfile/1.jpg')

    img1 = Image.open('./tempfile/1.jpg')
    img2 = Image.open('./pythontab.jpg')
    h1 = img1.histogram()
    h2 = img2.histogram()

    diff = math.sqrt(reduce(operator.add,  list(
        map(lambda a, b: (a-b)**2, h1, h2)))/len(h1))
    assert diff < 100

    # 5. quite the test application
    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    test_search_img()
