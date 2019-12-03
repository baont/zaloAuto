import selenium
import time
import base64
import requests
import urllib.request
import os
import atexit
# Using Chrome to access web
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from flask import Flask
from flask import jsonify
from flask import request
from flask import send_file
from flask import Response
from random import randrange
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(executable_path='.\chromedriver.exe')
# Open the website
driver.get('https://chat.zalo.me/')
print("Listening!")
@app.route('/getavatar')
def getAvatar():
    userPhoneNumb = request.args.get('phone')
    if not userPhoneNumb:
        return 'Need api param!'
    try:
        inviteBtn = driver.find_element_by_id("inviteBtn")
        inviteBtn.click()
        inputForm = driver.find_element_by_id("findFriend")
        inputField = inputForm.find_elements_by_tag_name("input")
        inputField[0].clear()
        inputField[0].send_keys(userPhoneNumb +'\n')
        try:
            userAvatar = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="profilePhoto"]/div[1]/div/div')))
            backgroundUrlString = userAvatar.value_of_css_property(
                "background-image")
            backgroundUrlString = backgroundUrlString.strip()
            closeBtn =  WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app-page"]/div[3]/div/div/div[1]/span[2]')))
            print(closeBtn)
            closeBtn.click()
            if backgroundUrlString:
                tokens = backgroundUrlString.split('url("')
                if tokens:
                    backgroundUrlString = tokens[1].replace('")', '')
                    return Response(requests.get(backgroundUrlString), mimetype="image/jpg")
            return 'This user has no avatar!'
        except:
            closeBtn =  WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app-page"]/div[4]/div/div/div[1]/span[2]')))
            closeBtn.click()
            return 'Invalid phone number!'
    except:
        return 'Login needed'

# for schedule test

# def callApi():
#     url = 'http://localhost:5001/getavatar?phone=038310405' + str(randrange(10))
#     response = requests.get(url)
#     print(response)
# sched = BackgroundScheduler(daemon=True)
# sched.add_job(callApi,'interval',seconds=10)
# sched.start()

