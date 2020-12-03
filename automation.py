from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

# enter text into the textbox, then press enter
def enterText(driver, textbox, text):
    time.sleep(0.25)
    textbox.send_keys(text)
    textbox.send_keys(Keys.RETURN)

productPage = input('Please enter the Amazon link to the product: ')
buyNowBtnExists = input('Does the product have the Buy Now button? If not, the Add to Cart button will be used instead. (y/n): ') == 'y'
refreshInterval = input('Please enter how often the page will refresh in seconds: ')

# open the browser and open the link
dir = os.getcwd()
print(dir)
browser = webdriver.Chrome(dir+'/chromedriver')
browser.maximize_window()
browser.get('https://www.amazon.com')

# sign in
with open('login_info.txt') as file: # get login info
    login = file.readlines()
    # remove newline at the end
    email = login[0].split(': ')[1].rsplit()
    password = login[1].split(': ')[1]

accountBtn = browser.find_element_by_id('nav-link-accountList')
accountBtn.click()
emailBox = browser.find_element_by_name('email')
enterText(browser, emailBox, email)
passwordBox = browser.find_element_by_name('password')
enterText(browser, passwordBox, password)
time.sleep(1)
# enter the password again if it asks again
if 'Two-Step Verification' not in browser.title:
    passwordBox = browser.find_element_by_name('password')
    enterText(browser, passwordBox, password)

# wait for the home page redirection
while 'Amazon.com' not in browser.title:
    continue

# check if signing in was successful
accountBtn = browser.find_element_by_id('nav-link-accountList')
assert 'Hello, Sign in' not in accountBtn.text

# turn on 1-Click
if buyNowBtnExists:
    browser.get('https://www.amazon.com/cpe/yourpayments/settings/manageoneclick?ref_=v1c_title')
    switch = browser.find_element_by_class_name('a-switch-control')
    switch.click()
    time.sleep(1)

browser.get(productPage) # go to the product page

print('The page will refresh every ' + refreshInterval + ' seconds until the item becomes available.')

# buy or put item in cart
# keep refreshing the page if the item is out of stock
while True:
    try:
        buyBtn = browser.find_element_by_id('buy-now-button') if buyNowBtnExists else browser.find_element_by_id('add-to-cart-button')
        buyBtn.click()
        time.sleep(3)
        browser.switch_to.frame(browser.find_element_by_id('turbo-checkout-iframe'))
        buyBtn = browser.find_element_by_id('turbo-checkout-pyo-button')
        buyBtn.click() # buy the product

        if buyNowBtnExists:
            print('Purchase successful!')
        else:
            print('In checkout screen. Please proceed with the purchase.')
        break
    except Exception as e:
        print(e)
        time.sleep(int(refreshInterval))
        browser.refresh()

time.sleep(2)
browser.get('https://www.amazon.com/gp/css/order-history?ref_=nav_orders_first')
input('Press any key to quit. ')
browser.close()