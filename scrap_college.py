from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import requests
import pandas as pd


firefox_profile = webdriver.FirefoxProfile()
#firefox_profile.set_preference('permissions.default.image', 2)
#firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

browser = webdriver.Firefox(firefox_profile=firefox_profile)
session_url = browser.command_executor._url      
session_id = browser.session_id 

def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver


if __name__ == "__main__":
    
    url = 'https://auth.geeksforgeeks.org/colleges/0/'
    pages = 36

    colleges = []
    for page in range(0,pages):
        url = 'https://auth.geeksforgeeks.org/colleges/' + str(page) + '/'
        soup = BeautifulSoup(requests.get(url).content,'lxml')
        try:         
            print ("Writing page ", page+1)
            for row in soup.findAll('table')[0].tbody.findAll('tr'):
                first_column = row.findAll('td')[0].text
                colleges.append(first_column)
            df = pd.DataFrame(colleges, columns=["colummn"])
            df.to_csv('college_list.csv', mode='a', header=False, index=False)
        except:
            print ("Skipping page ", page)