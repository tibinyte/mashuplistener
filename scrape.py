from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup
import time
import json
import asyncio

with open('config.json', 'r') as config_file:
    config = json.load(config_file)


#proxy_ip_port = '67.43.227.227:25481'

#proxy = Proxy()
#proxy.proxy_type = ProxyType.MANUAL
#proxy.http_proxy = proxy_ip_port
#proxy.ssl_proxy = proxy_ip_port

#capabilities = webdriver.DesiredCapabilities.CHROME
#proxy.add_to_capabilities(capabilities)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')

service = Service('/usr/lib/chromium-browser/chromedriver')

driver = webdriver.Chrome(service=service, options=chrome_options
                          #,desired_capabilities=capabilities
                          )

if config['login'] == True:
    driver.get("https://codeforces.com/enter?back=%2F")

    username = driver.find_element(By.ID, "handleOrEmail")
    password = driver.find_element(By.ID, "password")

    username.send_keys(config['cfHandle'])
    password.send_keys(config['cfPassword'])

    driver.find_element(By.CSS_SELECTOR, "input.submit").click()

def scrapeSubmissions(gymlink):
    driver.get(gymlink)
    page_source = driver.page_source

    if not driver.title:
       print("HTTP request failed.")
       return []
    
    print(driver.title)

    soup = BeautifulSoup(page_source, 'html.parser')

    submission_elements = soup.find_all('tr', {'data-submission-id': True})

    submissions = []

    # Loop through the found elements and do something with them
    for submission in submission_elements:
        # Extracting submission author
        author_element = submission.find(class_='rated-user')
        author = author_element.text if author_element else None

        # Extracting verdict
        verdict_element = submission.find(class_='status-cell')
        verdict_span = verdict_element.find('span') if verdict_element else None
        verdict = verdict_span.text.strip()
                

        # Extracting time consumed
        time_consumed_element = submission.find(class_='time-consumed-cell')
        time_consumed = time_consumed_element.text.strip() if time_consumed_element else None

        # Extracting memory consumed
        memory_consumed_element = submission.find(class_='memory-consumed-cell')
        memory_consumed = memory_consumed_element.text.strip() if memory_consumed_element else None

        # Extracting problem name
        problem_element = submission.find(href=lambda x: x and "/problem/" in x)
        problem_name = problem_element.text.strip() if problem_element else None

        # Extracting language
        language = submission.find('td', {'class': 'status-party-cell'}).find_next('td',  {'class': 'status-small'}).find_next('td').text.strip()

        # Extracting submission ID
        submission_id = submission['data-submission-id'] if 'data-submission-id' in submission.attrs else None

        submission_info = {
            "id": submission_id,
            "author": author,
            "verdict": verdict,
            "time": time_consumed,
            "memory": memory_consumed,
            "problem": problem_name,
            "lang": language
        }
        
        submissions.append(submission_info)
    return submissions

async def scrapeSubmissions_async(url):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, scrapeSubmissions, url)
    return result