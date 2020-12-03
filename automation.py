from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

# enter text into the textbox, then press enter
def enterText(driver, textbox, text):
    time.sleep(0.25)
    textbox.send_keys(text)
    time.sleep(1)
    textbox.send_keys(Keys.RETURN)

productPage = input('Please enter the Amazon link to the product: ')
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

# approve sign in attempt
# manually do bot verification and two-step authentication
input('Enter any key after the authentication is done. ')

# check if signing in was successful
accountBtn = browser.find_element_by_id('nav-link-accountList')
assert 'Hello, Sign in' not in accountBtn.text

# browser.get('https://www.amazon.com/dp/B08FC6MR62?tag=nismain-20&linkCode=ogi&th=1&psc=1')
browser.get(productPage)

print('The page will refresh every ' + refreshInterval + ' seconds until the item becomes available.')

# put item in cart
# keep refreshing the page if the item is out of stock
while True:
    try:
        buyBtn = browser.find_element_by_id('buy-now-button')
        buyBtn.click()
        print('In checkout screen. Please proceed with the purchase.')
        input('Enter any key to quit. ')
        break
    except Exception as e:
        time.sleep(int(refreshInterval))
        browser.refresh()

browser.close()