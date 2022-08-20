import requests
import pandas as pd
from bs4 import BeautifulSoup

def connect_to_website(site_url):
    # USING REQUEST LIB TO GET ALL THE DATA OF PAGE
    response = requests.get(site_url)
    if response.status_code != 200:
        raise Exception('SITE CONNECTION FAILED !\n'.format(site_url))
    else:
        print('CONNECTED TO SITE SUCCESSFULLY.\n'.format(site_url))

    # USING BEAUTIFULSOUP TO PARSE THE DATA ACC TO HTML
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc

def row_number(lenght):
    row_no = int(input('ENTER THE ROW NUMBER OF TOPIC YOU WANT TO LOOK IN - '))
    if row_no >= 0 and row_no<lenght:
        return row_no
    else:
        print('YOU ENTERED AN OUT OF RANGE NUMBER')
        row_number(lenght)

def titles(doc):

    # searching the required class and tag, and appending the result into title list and returning the list
    title_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p', {'class': title_class})
    topic_titles_list = []
    for item in topic_title_tags:
        topic_titles_list.append(item.text)
    return topic_titles_list

def description(doc):

    # searching the required class and tag, and appending the result into description list and returning it
    description_class = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = doc.find_all('p', {'class': description_class})
    topic_description_list = []
    for item in topic_desc_tags:
        topic_description_list.append(item.text.strip())
    return topic_description_list

def urls(doc):

    # searching the required class and tag, and appending the result into url list and returning it
    url_class = 'no-underline flex-1 d-flex flex-column'
    topic_link_tags = doc.find_all('a', {'class':url_class })
    topic_urls_list = []
    base_url = 'https://github.com'
    for tag in topic_link_tags:
        topic_urls_list.append(base_url + tag['href'])
    return topic_urls_list

def topic_information(doc):

    # creating a dictionary of title,desc,url and then creating and returning panda dataframe for it
    topics_dict = {
        'TITLE': titles(doc),
        'DESCRIPTION': description(doc),
        'LINK': urls(doc)
    }
    return pd.DataFrame(topics_dict)

def username(doc):
    # searching the required class and tag, and appending the result into username list and returning it
    username_list = []
    h3_tags = doc.find_all('h3', {'class': 'f3 color-fg-muted text-normal lh-condensed'})

    for i in range(0, len(h3_tags)):
        a_tags = h3_tags[i].find_all('a')
        topic_username = a_tags[0].text.strip()
        username_list.append(topic_username)

    return username_list


def link(doc):
    # searching the required class and tag, and appending the result into repo url list and returning it
    repo_url_list=[]
    url = doc.find_all('a', {'class': 'text-bold wb-break-word'})

    for item in url:
        repo_url_name = item['href']
        repo_url_list.append(repo_url_name)

    return repo_url_list

def star_count(doc):
    # searching the required class and tag, and appending the result into star count list and returning it
    count_list = []
    star = doc.find_all('span',{'class':'Counter js-social-count'})

    for item in range(0, len(star)):
        count_list.append(star[item]['title'])

    return count_list

def subtopic_information(doc):
    subtopic_dict = {
        'USERNAME': username(doc),
        'REPO_LINK': link(doc),
        'STAR COUNT':star_count(doc)
    }
    return pd.DataFrame(subtopic_dict)

def explore_data(lenght):
    # this function enable user to look into individual dataframe of topic
    topic_number = row_number(lenght)
    required_topic_link = topic_dataframe._get_value(topic_number, 'LINK') + '?o=desc&s=stars'
    required_topic_name = topic_dataframe._get_value(topic_number, 'TITLE')
    parsed_topic_doc = connect_to_website(required_topic_link)
    subtopic_dataframe = subtopic_information(parsed_topic_doc)
    print('TOPIC NAME IS - ',required_topic_name)
    print(subtopic_dataframe)



# MAIN BODY OF CODE STARTS HERE

print('HELLO, \nIN THIS PROJECT WE ARE GOING TO SCRAPE github.com\n')

# CONNECTING TO THE SITE AND RETURNING A BEAUTIFULLSOUP TYPE PARSED DOCUMENT.
parsed_doc = connect_to_website('https://github.com/topics')

# CREATING PYTHON DATAFRAME FROM THE PARSED DOCUMENT
topic_dataframe = topic_information(parsed_doc)
print('FIRST ',len(topic_dataframe),'ROWS OF DATA ARE -\n')
print(topic_dataframe,'\n')

# ASKING TO CREATE CSV FILEs OF ALL TOPIC AND IT'S DATA
ans = input('DO YOU WISH TO CREATE CSV FILES OF ALL RECORDS ? (Y/N)\n')
if ans == 'Y' or ans == 'y':
    topic_dataframe.to_csv('GITHUB_TOPICS_DATA')
    print('CREATING CSV FILES....\n')

    for i in range(len(topic_dataframe)):
        topic_number = i

        # ADDING '?o=desc&s=stars' TO THE WHOLE LINK SO THAT REPOSITORIES APPEAR IN SORTED FORMAT
        required_topic_link = topic_dataframe._get_value(topic_number, 'LINK') + '?o=desc&s=stars'
        required_topic_name = topic_dataframe._get_value(topic_number, 'TITLE')
        parsed_topic_doc = connect_to_website(required_topic_link)
        subtopic_dataframe = subtopic_information(parsed_topic_doc)
        subtopic_dataframe.to_csv(required_topic_name)
        print('CREATED CSV OF TOPIC NUMBER ',i)
    print("CREATED CSVs OF ALL TOPICS ..")

# ASKING USER IF HE/SHE WANTS TO LOOK INTO ANY INDIVIDUAL REPOSITORY OR TOPIC
next_step = input('DO YOU WANT TO LOOK INTO ANY INDIVIDUAL TOPIC DATA ? (Y/N)')
while next_step == 'y' or next_step == 'Y':
    explore_data(len(topic_dataframe))
    next_step = input('DO YOU WANT TO LOOK INTO ANY INDIVIDUAL TOPIC DATA ? (Y/N)')