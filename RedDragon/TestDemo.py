#coding=utf-8
from selenium import webdriver
import os
import time
import random
c_path = os.path.abspath(r"D:\chromedriver\chromedriver.exe")  #PhantomJS凉了

browser = webdriver.Chrome(c_path)
browser.get('http://127.0.0.1/movie')
time.sleep(1)
browser.find_element_by_id("username").send_keys("sunheqing")
time.sleep(1)
browser.find_element_by_id("password").send_keys("www")
time.sleep(1)
browser.find_element_by_id("submit").click()
for i in range(0,6):
    browser.find_element_by_id("Capa_1").click()
    time.sleep(1)
browser.find_element_by_xpath('//a[@href="movie/recommond"]').click()
time.sleep(1)
id = random.randint(10,900)
browser.find_element_by_id("id").send_keys(str(id))
time.sleep(1)
browser.find_element_by_id("submit").click()