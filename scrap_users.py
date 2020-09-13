from bs4 import BeautifulSoup
import requests
import pandas as pd

pages = 154

for page in range(1,pages):
    try:
        url = 'https://auth.geeksforgeeks.org/users?page={}&sortby=popular'.format(page)
        users = []
        soup = BeautifulSoup(requests.get(url).content, 'lxml')

        divs = soup.find_all('div', {'class':'ua--card-wide mdl-card mdl-shadow--4dp mdl-card--border'})
        for div in divs:
            user_title = div.find('div',{'class':'mdl-card__title ua-title'})
            user = user_title.find('h2', {'class':'mdl-card__title-text ua-ellipsis'}).text
            user_link = user_title.find('a')['href']
            users.append([user, user_link])
        #print (users_link)
        
        df = pd.DataFrame(users, columns=["user", "user_link"])
        df.to_csv('users.csv', mode='a', header=False, index=False)
        
    except:
        print ('Skipping page', page)
    #break