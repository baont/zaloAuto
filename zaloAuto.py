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
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(executable_path='.\chromedriver.exe')
# Open the website
driver.get('https://chat.zalo.me/')
print("Listening!")


def closeSearchBox():
    closeBtn = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'modal-close')))
    closeBtn.click()


@app.route('/getavatar')
def getAvatar():
    userPhoneNumb = request.args.get('phone')
    if not userPhoneNumb:
        return 'Need api param!'

    try:
        inviteBtn = driver.find_element_by_id("inviteBtn")
        inviteBtn.click()
    except:
        try:
            inputForm = driver.find_element_by_id("findFriend")
        except:
            return "Login needed"
        try:
            closeSearchBox()
        except:
            return "Cannot detect close button"
        inviteBtn = driver.find_element_by_id("inviteBtn")
        inviteBtn.click()
    inputForm = None
    try:
        inputForm = driver.find_element_by_id("findFriend")
    except:
        return "Cannot find input form"
    try:
        inputField = inputForm.find_elements_by_tag_name("input")
        inputField[0].clear()
        inputField[0].send_keys(userPhoneNumb + '\n')
    except:
        return "Cannot find input field"
    userAvatar = None
    try:
        userAvatar = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="profilePhoto"]/div[1]/div/div')))
    except:
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#lan-list > div > div:nth-child(1) > div > div')))
            try:
                closeSearchBox()
            except:
                return "Cannot detect close button"
            return "This phone number had been not registered yet"
        except:
            try:
                WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#findFriend > div:nth-child(2) > div')))
                try:
                    closeSearchBox()
                except:
                    return "Cannot detect close button"
                return "This phone number had been not registered yet"
            except:
                return "This user has no avatar!"
    backgroundUrlString = userAvatar.value_of_css_property(
        "background-image")
    backgroundUrlString = backgroundUrlString.strip()
    try:
        closeSearchBox()
    except:
        return "Cannot detect close button"
    if backgroundUrlString:
        tokens = backgroundUrlString.split('url("')
        if tokens:
            backgroundUrlString = tokens[1].replace('")', '')
            return Response(requests.get(backgroundUrlString), mimetype="image/jpg")
    return 'This user has no avatar!'


if __name__ == "__main__":
    app.run()
# for schedule test

# def callApi():
#     url = 'http://localhost:5001/getavatar?phone=038310405' + str(randrange(10))
#     response = requests.get(url)
#     print(response)
# sched = BackgroundScheduler(daemon=True)
# sched.add_job(callApi,'interval',seconds=10)
# sched.start()
