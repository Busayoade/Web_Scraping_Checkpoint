#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup

def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None

def parse_html_content(html_content):
    return BeautifulSoup(html_content, 'html.parser')

#Extract article title
def extract_article_title(soup):
    return soup.find('h1').text

#Extract article text with heading
def extract_article_text_with_headings(soup):
    article_data = {}
    paragraphs = soup.find_all(['h2', 'p'])
    current_heading = ''
    
    for element in paragraphs:
        if element.name == 'h2':
            current_heading = element.text
            article_data[current_heading] = []
        elif element.name == 'p':
            article_data[current_heading].append(element.text)
    
    return article_data

#Collect links redirecting to other wikipedia pages
def collect_wikipedia_links(soup):
    wiki_links = []
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('/wiki/') and ':' not in link['href']:
            wiki_links.append(link['href'])
    return wiki_links

#Wrap all function into a single function
def scrape_wikipedia_page(wikipedia_link):
    html_content = get_html_content(wikipedia_link)
    if html_content:
        soup = parse_html_content(html_content)
        title = extract_article_title(soup)
        article_text = extract_article_text_with_headings(soup)
        links = collect_wikipedia_links(soup)
        
        return {
            'title': title,
            'article_text': article_text,
            'links_to_other_pages': links
        }
    else:
        return None

#Test the function
# Test the function with a Wikipedia page link
wikipedia_link = 'https://en.wikipedia.org/wiki/Artificial_intelligence'
result = scrape_wikipedia_page(wikipedia_link)

if result:
    print(f"Title: {result['title']}\n")
    print("Article Text with Headings:")
    for heading, paragraphs in result['article_text'].items():
        print(f"\n{heading}:")
        for paragraph in paragraphs:
            print(paragraph)
    print("\nLinks to Other Wikipedia Pages:")
    for link in result['links_to_other_pages']:
        print(link)
else:
    print("Failed to scrape the Wikipedia page.")




# In[ ]:





# In[ ]:




