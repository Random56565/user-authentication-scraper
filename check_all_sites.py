# library imports
import requests
from selenium import webdriver                  ## to control the browser
from selenium.webdriver.common.keys import Keys ## to simulate key presses
from selenium.webdriver.common.by import By     ## to locate elements within a document
from selenium.webdriver.chrome.service import Service
import argparse # import library for parsing arguments from command line

# file imports
from check_passwords.py import *
from check_captcha.py import *
from check_cookies.py import *
from check_oauth.py import *

## helper functions
def get_login_links(by, value):
    ''' finds and returns matching login-related links on the web page (where sso may be)'''

    login_links = []
    login_terms = {'login', 'log in', 'signin', 'sign in'}

    ## get all links
    links = driver.find_elements(by, value)           
    if len(links) > 0: print(f'{len(links)} links found')
    for link in links:
        url = link.get_attribute('href')                        ## isolate the url
        if url and any(term in url for term in login_terms):    ## append only login links
            login_links.append(url)

    return login_links

def write_file(file, fido2, oauth, captcha, cookies, passwords, url, login):
    ''' writes website and login links to a txt file '''

    with open(file, 'a') as f: ## if running from root
        if login:
            f.write(f'Login url: {url}\n')  
        else:
            f.write(f'\n\nWebsite:{url}\n')         ## website url header
        f.write(f'FIDO2: ')
        f.write(f'{fido2}\n') 
        f.write(f'OAuth2: ')
        f.write(f'{oauth}\n') 
        f.write(f'Captcha: ')
        f.write(f'{captcha}\n') 
        f.write(f'Cookies: ')
        f.write(f'{cookies}\n') 
        f.write(f'Passwords: ')
        f.write(f'{passwords}\n') 

def start_file(file):
    with open(file, 'w') as f:
        f.write("Analysis of Authorization Methods:")

if __name__ == '__main__':
    # set up command line argument parsing for -c and -t arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', default='check_oauth.txt')
    parser.add_argument('-b', default='Safari')
    args = parser.parse_args()

    # clear report file and start new
    start_file(args.o)

    ## create a web driver instance (only few browsers are supported)
    options = webdriver.ChromeOptions()
    if (args.b == "Safari"):
        driver = webdriver.Safari()     ## opens a browser window
        options = webdriver.SafariOptions()
    elif (args.b == "Chrome"):
        driver = webdriver.Chrome()     ## opens a browser window
    options.add_argument('--enable-javascript')

    ## other variables
    websites = {'https://www.activision.com/', 'https://www.formula1.com/', 'https://www.python.org',
                 'https://www.ebay.com/', 'https://soundcloud.com/', 'https://bestbuy.com/', 
                 'https://twitter.com/i/flow/login', 'https://en.wikipedia.org/'}                

    ## choose a site for testing
    for site in websites:

        ## load a website
        driver.get(site)
        print(f'url: {driver.current_url}')

        # -- finding oauth -- ##
        oauth = find_oauth(driver, site) 
        fido2 = find_fido2(driver, site)
        cap = find_captcha(driver, site)
        cookies = find_cookies(driver, site)
        pwd = find_passwords(driver, site)

        ## write to txt file
        write_file(args.o, fido2, oauth, cap, cookies, pwd, site, False)

        ## -- finding links to a login page -- ##


        ## get all links (by tag name)
        login_links = get_login_links(By.TAG_NAME, 'a')

        ## get all links (by class name, if tag name did not work)
        if len(login_links) == 0: login_links = get_login_links(By.CLASS_NAME, 'a')
        print(f'{len(login_links)} login links found')


        ## -- navigating to the login page -- ##

        # try all login links
        if login_links: 
            for link in login_links:
                try:
                    driver.get(link)
                    print(f'new url: {driver.current_url}')

                    # -- finding all authentication methods -- ##
                    oauth = find_oauth(driver, link) 
                    fido2 = find_fido2(driver, link) 
                    cap = find_captcha(driver, link)
                    cookies = find_cookies(driver, link)
                    pwd = find_passwords(driver, link)

                    ## write to txt file
                    write_file(args.o, fido2, oauth, cap, cookies, pwd, link, True)

                except:
                    continue         

        ## -- program exit -- ##

        ## close the tab
        driver.close()

        ## close the window
        driver.quit()
