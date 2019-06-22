#!/usr/bin/env python3

import os
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait


user = os.environ['GITHUB_USER']
password = os.environ['GITHUB_PASSWORD']

zenhub_login_url = "https://app.zenhub.com/login"
burndown_chart_url = "https://app.zenhub.com/workspaces/content-engineering-tech-team-5af1f4cc12da5e6d74331b60/reports/burndown?milestoneId=4039659"

login_button_locator = (By.CSS_SELECTOR, "#app > div > div > div > div:nth-child(2) > div > button")
login_user_locator = (By.ID, "login_field")
login_password_locator = (By.ID, "password")
login_submit_locator = (By.CSS_SELECTOR, "input.btn.btn-primary.btn-block")

openstax_org_locator = (By.XPATH, "//*[contains(text(), 'openstax')]")
burndown_title_locator = (By.CLASS_NAME, "zhc-milestone-title")
loading_locator = (By.CLASS_NAME, "zhc-loading")
burndown_svg_locator = (By.CLASS_NAME, "zhc-chart-svg")

driver = webdriver.Chrome()

driver.maximize_window()

height = driver.get_window_size()["height"]
width = 1024

driver.set_window_size(width, height)

driver.get(zenhub_login_url)

driver.implicitly_wait(2)

login_button = driver.find_element(*login_button_locator)

login_button.click()

driver.implicitly_wait(2)

login_user_input = driver.find_element(*login_user_locator)
login_password_input = driver.find_element(*login_password_locator)
login_submit_button = driver.find_element(*login_submit_locator)

login_user_input.send_keys(user)
login_password_input.send_keys(password)
login_submit_button.click()

driver.implicitly_wait(2)

driver.get(burndown_chart_url)

WebDriverWait(driver=driver, timeout=90).until_not(visibility_of_element_located(loading_locator))
WebDriverWait(driver=driver, timeout=90).until(visibility_of_element_located(burndown_svg_locator))

png = driver.get_screenshot_as_png()

driver.close()

im = Image.open(BytesIO(png))

im = im.resize(size=(width, height), resample=Image.BILINEAR)

left = 65
top = 360
right = left + 950
bottom = top + 530

im = im.crop((left, top, right, bottom))

im.save('screenshot.png')
