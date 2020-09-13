from bs4 import BeautifulSoup
import pandas as pd
import requests

def scrap_articles(user_link):
    articles = []
    article_links = []

    link = user_link + 'articles/'
    soup = BeautifulSoup(requests.get(link).content, 'lxml')

    try:
        article_sec = soup.find_all('li', {'class':'contribute-li'})
        for article in article_sec:
            article_links.append(article.find('a')['href'])
            articles.append(article.find('a').text)
    except:
        pass
    return articles,article_links

def get_name(user_link):
    link = user_link + 'practice/'
    soup = BeautifulSoup(requests.get(link).content, 'lxml')

    user = soup.find('span', {'class':'mdl-layout-title userName'}).text
    college = soup.find('div', {'class':'mdl-cell mdl-cell--9-col mdl-cell--12-col-phone textBold'}).text

    return user, college

def scrap_profile(user_link):
    users = []
    colleges = []
    category = []
    problems  = []
    problem_link = []
    articles = None
    
    link = user_link + 'practice/'
    soup = BeautifulSoup(requests.get(link).content, 'lxml')

    user = soup.find('span', {'class':'mdl-layout-title userName'}).text
    college = soup.find('div', {'class':'mdl-cell mdl-cell--9-col mdl-cell--12-col-phone textBold'}).text
    
    school_section = soup.find('section', {'id':'School'})
    basic_section = soup.find('section', {'id':'Basic'})
    easy_section = soup.find('section', {'id':'Easy'})
    medium_section = soup.find('section', {'id':'Medium'})
    hard_section = soup.find('section', {'id':'Hard'})
    contribute_section  = soup.find('section', {'id':'fullCode'})    
    contribute_function = soup.find('section',{'id':'functionCode'})

    try:
        problem_sec = school_section.find_all('li',{'class':'mdl-cell mdl-cell--6-col mdl-cell--12-col-phone'})
        for problem in problem_sec:
            users.append(user)
            colleges.append(college)
            problem_link.append(problem.find('a')['href'])
            problems.append(problem.find('a').text)
            category.append('practice')
    except:
        pass

    try:
        basic_sec = basic_section.find_all('li',{'class':'mdl-cell mdl-cell--6-col mdl-cell--12-col-phone'})
        for problem in basic_sec:
            users.append(user)
            colleges.append(college)
            problem_link.append(problem.find('a')['href'])
            problems.append(problem.find('a').text)
            category.append('practice')
    except:
        pass

    try:
        easy_sec = easy_section.find_all('li',{'class':'mdl-cell mdl-cell--6-col mdl-cell--12-col-phone'})
        for problem in easy_sec:
            users.append(user)
            colleges.append(college)
            problem_link.append(problem.find('a')['href'])
            problems.append(problem.find('a').text)
            category.append('practice')
    except:
        pass

    try:
        medium_sec = medium_section.find_all('li',{'class':'mdl-cell mdl-cell--6-col mdl-cell--12-col-phone'})
        for problem in medium_sec:
            users.append(user)
            colleges.append(college)
            problem_link.append(problem.find('a')['href'])
            problems.append(problem.find('a').text)
            category.append('practice')
    except:
        pass

    try:
        hard_sec = hard_section.find_all('li',{'class':'mdl-cell mdl-cell--6-col mdl-cell--12-col-phone'})
        for problem in hard_sec:
            users.append(user)
            colleges.append(college)
            problem_link.append(problem.find('a')['href'])
            problems.append(problem.find('a').text)
            category.append('practice')
    except:
        pass

    try:
        problem_sec = contribute_section.find_all('li', {'class':'mdl-cell mdl-cell--6-col mdl-cell--12-col-phone'})
        for problem in problem_sec:
            users.append(user)
            colleges.append(college)
            problem_link.append(problem.find('a')['href'])
            problems.append(problem.find('a').text)
            category.append('contribute')
    except:
        articles = False
        pass
    
    try:
        problem_sec = contribute_function.find_all('li', {'class':'mdl-cell mdl-cell--6-col mdl-cell--12-col-phone'})
        for problem in problem_sec:
            users.append(user)
            colleges.append(college)
            problem_link.append(problem.find('a')['href'])
            problems.append(problem.find('a').text)
            category.append('contribute')
    except:
        articles = False
        pass
    #print (problems)
    return users, colleges, problems, problem_link, category, articles

if __name__ == "__main__":
    
    df1 = pd.read_csv("users_data.csv", index_col=False, header=None)
    for i in range(1505,1625):
        user = []
        college = []
        problems = []
        problem_link = []
        category = []
        articles = []
        article_links = []
        row = []
        contribute_state = None
        
        link = str(df1[1][i]).strip('articles')
        print ("Writing ", link)

        user, college, problems, problem_link, category, contribute_state = scrap_profile(link)
        
        if not contribute_state:
            articles, article_links = scrap_articles(link)
            if len(user)>1:
                current_user= user[0]
                current_college = college[0]
                current_category = 'article'
            else:
                current_user, current_college = get_name(link)
                current_category = 'article'

            for i in range(0,len(articles)-1):
                user.append(current_user)
                college.append(current_college)
                category.append(current_category)
                problems.append(articles[i])
                problem_link.append(article_links[i])
                
        for i in range(0,len(user)-1):
            row.append([user[i], college[i], category[i], problems[i], problem_link[i]])
        
        df2 = pd.DataFrame(row, columns=["user", "college", "category", "problems", "problem_link"])
        df2.to_csv('questions_data_1.csv', mode='a', index=False, header=False)
        
