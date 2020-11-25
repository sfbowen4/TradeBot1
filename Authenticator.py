import time
import urllib
import requests
from Credentials import username, password, client_id, SQ1, SQ2, SQ3, SQ4
from splinter import Browser

#Browser stuff
executable_path = {'executable_path': r'C:\Users\sfbow\Desktop\chromedriver'}
browser = Browser('chrome', **executable_path, headless = False)

#URL components
method = 'GET'
url = 'https://auth.tdameritrade.com/auth?'
client_code = client_id + '@AMER.OAUTHAP'
payload = {'response_type':'code','redirect_uri':'https://localhost/test','client_id':client_code}

#build the url
built_url = requests.Request(method, url, params = payload).prepare()
built_url = built_url.url

#go to the url
browser.visit(built_url)
time.sleep(3)

#define elements to pass through the form
payload = {'username':username, 'password':password}
browser.find_by_id("username0").first.fill(payload['username'])
browser.find_by_id("password").first.fill(payload['password'])
browser.find_by_id("accept").first.click()
time.sleep(1)

#2FA and Security Question
browser.find_by_text('Can\'t get the text message?').first.click()
time.sleep(1)
browser.find_by_value("Answer a security question").first.click()

if browser.is_text_present('What is your paternal grandmother\'s first name?'):
    browser.find_by_id('secretquestion0').first.fill(SQ1)

elif browser.is_text_present('What is your best friend\'s first name?'):
    browser.find_by_id('secretquestion0').first.fill(SQ2)

elif browser.is_text_present('In what city was your high school? (Enter full name of city only.)'):
    browser.find_by_id('secretquestion0').first.fill(SQ3)

elif browser.is_text_present('What was the last name of your favorite teacher in your final year of high school?'):
    browser.find_by_id('secretquestion0').first.fill(SQ4)


#Submit security question
browser.find_by_id('accept').first.click()
time.sleep(1)

#Trust this device
browser.find_by_xpath('/html/body/form/main/fieldset/div/div[1]/label').first.click()
browser.find_by_id('accept').first.click()
time.sleep(1)

#Accept and stuff
browser.find_by_id('accept').first.click()
time.sleep(1)

#store URL
new_url = browser.url
parse_url = urllib.parse.unquote(new_url.split('code=')[1])

#Quit Browser
browser.quit()

#part 2 of authentication
url = r'https://api.tdameritrade.com/v1/oauth2/token'
headers = {"Content-Type":"application/x-www-form-urlencoded"}
payload = {'grant_type': 'authorization_code', 'access_type': 'offline', 'code': parse_url, 'client_id':client_id, 'redirect_uri':'https://localhost/test'}

authReply = requests.post(url, headers = headers, data = payload)

decoded_content = authReply.json()

access_token = decoded_content['access_token']
refresh_token = decoded_content['refresh_token']
auth_token_life = decoded_content['expires_in']

AuthorizedToken = {'Authorization': "Bearer {}".format(access_token)}

def RefreshAuth():
    global refresh_token
    #Refresh Auth
    url = r'https://api.tdameritrade.com/v1/oauth2/token'
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    payload = {'grant_type': 'refresh_token', 'refresh_token': refresh_token, 'client_id':client_id, 'redirect_uri':'https://localhost/test'}
    authReply = requests.post(url, headers = headers, data = payload)
    decoded_content = authReply.json()
    access_token = decoded_content['access_token']

    global AuthorizedToken
    AuthorizedToken = {'Authorization': "Bearer {}".format(access_token)}