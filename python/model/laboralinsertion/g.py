
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.PhantomJS()
try:
    browser.get('http://gmail.com')
    emailElem = browser.find_element_by_id('Email')
    emailElem.send_keys('insercionlaboralfce@gmail.com')
    nextButton = browser.find_element_by_id('next')
    nextButton.click()

    w = (By.ID, 'Passwd')
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located(w))

    passwordElem = browser.find_element_by_id('Passwd')
    passwordElem.send_keys('insercionlaboral511')
    signinButton = browser.find_element_by_id('signIn')
    signinButton.click()

finally:
    browser.quit()
