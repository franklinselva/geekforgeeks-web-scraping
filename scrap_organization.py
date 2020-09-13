from bs4 import BeautifulSoup
import requests
import pandas as pd

if __name__ == "__main__":
    for i in range(0,2):
        url = 'https://auth.geeksforgeeks.org/organizations/{}'.format(i)
        organization_list = []
        soup = BeautifulSoup(requests.get(url).content, 'lxml')

        divs = soup.find_all('div', {'class':'mdl-cell mdl-cell--3-col mdl-cell--4-col-tablet mdl-cell--12-col-phone text-center alternate-bg'})
        for div in divs:
            organizations = div.find('a')
            organization_list.append(organizations.text)

        df = pd.DataFrame(organization_list, columns=["organization"])
        df.to_csv('organization_list.csv', mode='a', header=False, index=False)