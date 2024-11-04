## a basic program that takes in a webpage, scrapes its content, navigates to the
## login page, then checks if the user can sign in via OAuth

## ---------------------------------------------------------------- ##

## imports 
from selenium import webdriver                  ## to control the browser
from selenium.webdriver.common.keys import Keys ## to simulate key presses
from selenium.webdriver.common.by import By     ## to locate elements within a document

## ---------------------------------------------------------------- ##

## helper function
def write_file():
    ''' writes website and login links to a txt file '''

    with open('./oauth/check-oauth.txt', 'w') as f: ## if running from root
        f.write(f'{website}\n')         ## website url header
        for provider in providers:
            f.write(f'{provider}\n')    ## providers

## helper function
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
            print(url)

    return login_links

## helper function
def find_login_field(by):
    ''' finds matching login-related fields on the web page, returns True if found '''

    username_words = {'username', 'accountName', 'loginform', 'userid', 
                  'user', 'acctName', 'login'}
    
    ## look for username- and login-related words on the web page
    for word in username_words:
        username = driver.find_elements(by, word)
        if len(username) > 0:
            print(f'found login field -- password based authentication detected')
            return True
    
    return False


## helper function
def find_oauth(by):
    ''' finds matching  '''
    return find_providers(by)

## helper function
def find_providers(by):
    ''' searches for common OAuth provider names, returns an array of all matching names '''

    common_providers = {'google', 'ggl', 'facebook', 'twitter', 'github', 'linkedin',
                        'xbl', 'xbox', 'psn', 'playstation', 'battle', 'steam',
                        'apple', 'appl'}

    ## look for username- and login-related words on the web page
    for provider in common_providers:
        
        ## check if href link includes provider name anywhere within the string
        # found_providers = driver.find_elements(By.CSS_SELECTOR, f'[href*={provider}]')
        found_providers = driver.find_elements(By.CSS_SELECTOR, f'[{by}*={provider}]')
        if found_providers: providers.append(provider)

    if len(providers) > 0:
        print(f'oauth provider found -- sso authentication detected')
        
    return providers


## ---------------------------------------------------------------- ##

## create a web driver instance (only few browsers are supported)
driver = webdriver.Safari()     ## opens a browser window
options = webdriver.SafariOptions()
options.add_argument('--enable-javascript')

## other variables
website1 = 'https://www.activision.com/'                 
website2 = 'https://www.formula1.com/'      ## broken, since its html structure is weird
website3 = 'https://www.python.org'
website4 = 'https://www.ebay.com/'  ## doesn't always work, and only finds facebook
                                    ## (^ broken when blocked by bot-detection)
website5 = 'https://soundcloud.com/'
providers = []

## choose a site for testing
website = website1

## load a website
driver.get(website)
print(f'url: {driver.current_url}')


## -- finding links to a login page -- ##


## get all links (by tag name)
login_links = get_login_links(By.TAG_NAME, 'a')

## get all links (by class name, if tag name did not work)
if len(login_links) == 0: login_links = get_login_links(By.CLASS_NAME, 'a')
print(f'{len(login_links)} login links found')


## -- navigating to the login page -- ##


## click on the first login link
if login_links: 
    login_link = login_links[0]
    driver.get(login_link)
    print(f'new url: {driver.current_url}')


## -- finding oauth -- ##

## check if there are any oauth options (by id)
oauth_providers = find_oauth('href') 
if len(oauth_providers) == 0: 
    oauth_providers = find_oauth('onclick')  ## try searching by id otherwise
    oauth_providers = find_oauth('id')  ## try searching by id otherwise
    # print('found oauth by id')

## output negative results
# if not oauth_id:
if len(oauth_providers) == 0:
    print(f'no oauth options detected')

## write to txt file
write_file()


## -- program exit -- ##


## close the tab
driver.close()

## close the window
# driver.quit()

