import requests
# Using Chrome to access web
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from flask import Flask
from flask import request
from flask import Response
from apscheduler.schedulers.background import BackgroundScheduler
import time

app = Flask(__name__)
chrome_options = Options()
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
# driver = webdriver.Chrome(executable_path='.\chromedriver.exe')
driver = webdriver.Chrome()
driver.implicitly_wait(10) # seconds
# Open the website
driver.get('https://chat.zalo.me/')
print("Listening!")
isProcessing = False


@app.route('/getavatar')
def getAvatar():
    global isProcessing
    while isProcessing:
        print('wait for finish')
        time.sleep(1)

    isProcessing = True
    driver.refresh()
    userPhoneNumb = request.args.get('phone')
    if not userPhoneNumb:
        isProcessing = False
        return 'Need api param!'

    try:
        inviteBtn = driver.find_element_by_id("inviteBtn")
        inviteBtn.click()
    except:
        try:
            inputForm = driver.find_element_by_id("findFriend")
        except:
            isProcessing = False
            return "Login needed"
    inputForm = None
    try:
        inputForm = driver.find_element_by_id("findFriend")
    except:
        isProcessing = False
        return "Cannot find input form"
    try:
        inputField = inputForm.find_elements_by_tag_name("input")
        inputField[0].clear()
        inputField[0].send_keys(userPhoneNumb + '\n')
    except:
        isProcessing = False
        return "Cannot find input field"
    userAvatar = None
    try:
        userAvatar = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="profilePhoto"]/div[1]/div/div')))
    except:
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#lan-list > div > div:nth-child(1) > div > div')))
            isProcessing = False
            return "This phone number had been not registered yet"
        except:
            try:
                WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#findFriend > div:nth-child(2) > div')))
                isProcessing = False
                return "This phone number had been not registered yet"
            except:
                isProcessing = False
                return "This user has no avatar!"
    backgroundUrlString = userAvatar.value_of_css_property(
        "background-image")
    backgroundUrlString = backgroundUrlString.strip()
    if backgroundUrlString:
        tokens = backgroundUrlString.split('url("')
        if len(tokens) > 1:
            backgroundUrlString = tokens[1].replace('")', '')
            isProcessing = False
            return Response(requests.get(backgroundUrlString), mimetype="image/jpg")
    isProcessing = False
    return 'This user has no avatar!'

# Refresh page
def refreshPage():
    driver.refresh()
# Shedule job refresh page every 10 minute
sched = BackgroundScheduler(daemon=True)
sched.add_job(refreshPage,'interval', minutes=10)
sched.start()
if __name__ == "__main__":
    app.run()