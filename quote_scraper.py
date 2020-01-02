import csv 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import time

filepath = 'C:\\Users\\lakshya\\Documents\\My_Workspace\\Milestone Projects\\Selenium'
# Creating Dataset 
with open(f'{filepath}\\scraped_quotes.csv','a') as csv_file: 
    headings = ['Quote','Author','Topics'] 
    csv_writer = csv.writer(csv_file, delimiter='\t') 

    driver = webdriver.Chrome('C:\\Users\\lakshya\\Downloads\\chromedriver_win32\\chromedriver.exe')
    driver.maximize_window() 
    driver.get('https://www.brainyquote.com/quote_of_the_day')
    elem = driver.find_element_by_tag_name("body")

    no_of_pagedowns = 10

    while no_of_pagedowns: # Scroll down the page as much as possible to increase viewable HTML Code
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        no_of_pagedowns-=1 

    csv_writer.writerow(headings)

    # Quote, Author and Topics
    try: 
        quotes = driver.find_elements_by_css_selector("""div.col-xs-4.col-md-4 a[title="view quote"]""") 
        authors = driver.find_elements_by_css_selector("""div.col-xs-4.col-md-4 a[title="view author"]""")
        
        grouped_topics = []
        total_topics = driver.find_elements_by_css_selector('div.col-xs-4.col-md-4 div.qll-dsk-kw-box')
        for topic in total_topics:
            topics = topic.find_elements_by_css_selector('a.qkw-btn.btn.btn-xs.oncl_list_kc')
            grouped_topics.append([topic.text for topic in topics])
        
        for quote,author, topics in zip(quotes,authors, grouped_topics): 
            print('Quote: ', quote.text) 
            print('Author: ', author.text) 
            print('Topics: ', ",".join(topics) ) 
            print() # New line between every entry 
            
    except Exception as e:
        pass

    driver.quit()

    # Writing to CSV File 

    try: 
        for quote,author,topics in zip(quotes,authors,grouped_topics):
            csv_writer.writerow([quote,author, topics])
    except Exception as e: 
        pass 
       
# Reading Dataset for Manipulation 

with open(f'{filepath}\\scraped_quotes.csv') as csv_file: 
    csv_reader = csv.DictReader(csv_file, delimiter='\t') 
    
    def getQuote(topics):  # Function to get the most appropriate quote
        big = 0
        quote = 'No quote found'  # Default value in case no quote matched
        for line in csv_reader: # Goes over all lines in the CSV Line. Each line has keys 'Quote','Author','Topics'
            count = 0 
            for input_topic in topics: 
                if input_topic.capitalize() in line['Topics']: 
                    count += 1  # If the topic input by user is in the Topics of a quote, increment "Count"
            if count>big:  # Finding the line having the max value of "big" 
                big = count 
                quote = line['Quote']  # Setting quote as the quote of the line having max value of "big"
        
        return quote 
    
    input_topics = [i for i in input('Enter topics: ').split()] 
    print('Matched Quote: ' + getQuote(input_topics) ) 