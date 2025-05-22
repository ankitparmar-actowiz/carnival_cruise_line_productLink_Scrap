from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from seleniumwire.webdriver import Chrome
from fake_useragent import UserAgent
from curl_cffi import requests
import time, json, math

ua = UserAgent().random
options = {
    'request_storage': 'memory',
}
driver = Chrome(seleniumwire_options=options)

driver.get('https://tap5.myagentgenie.com/phillipcrane/')
driver.maximize_window()

while True:
    try:
        isDataLoad = driver.find_element(By.XPATH, '//div[@class="multiselect__tags"]/following::div[1][not(contains(@style, "display: none;"))]//span[contains(text(), "Carnival Cruise Line")]')
    except:
        isDataLoad = None

    if not isDataLoad:
        print('.', end='')
        time.sleep(1)
    else:
        break
time.sleep(2)

clickCruise = driver.find_elements(By.XPATH, '//div[@class="multiselect__tags"]')[3].click()
time.sleep(1)

findCarnivalCruiseLine = driver.find_elements(By.XPATH, '//div[@class="multiselect__tags"]/following::div[1][not(contains(@style, "display: none;"))]//span[contains(text(), "Carnival Cruise Line")]')[0]
driver.execute_script('arguments[0].click(); ', findCarnivalCruiseLine)
time.sleep(2)

clickSearch  = driver.find_elements(By.XPATH, '//button[@id="SearchBTN"]')[0]
driver.execute_script('arguments[0].click(); ', clickSearch)
time.sleep(1)

driver.close()

driver.switch_to.window(driver.window_handles[-1])

while True:
    try:
        totalItineries = driver.find_element(By.XPATH, '//*[@class="itinerary-count"]')
    except:
        totalItineries = None

    if not totalItineries:
        print('.', end='')
        time.sleep(1)
    else:
        break
time.sleep(2)

actions = ActionChains(driver)

totalData = int(driver.find_element(By.XPATH, '//*[@class="itinerary-count"]').text.strip().split(' ',1)[0])
print('totalData: ', totalData)

carnivalCruiseLineID = driver.current_url.split('siid=', 1)[-1].split('&', 1)[0]

tempCookies = driver.get_cookies()

cookies = {cookie['name']: cookie['value'] for cookie in tempCookies}

for request in driver.requests:
    uniquetid = request.headers['uniquetid']
    if uniquetid:
        break

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'devicetype': 'Desktop',
    'languageid': '1',
    'origin': 'https://book.myagentgenie.com',
    'priority': 'u=1, i',
    'referer': f'https://book.myagentgenie.com/swift/cruise?siid={carnivalCruiseLineID}&searchcruise=1&cruiseline=1&durations=&destinationtype=All',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'siteitemid': f'{carnivalCruiseLineID}',
    'uniquetid': f'{uniquetid}',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
}

json_data = {
    'filters': [
        {
            'key': 'cruiselineId',
            'values': [
                '1',
            ],
        },
        {
            'key': 'destinationType',
            'value': 'All',
        },
        {},
    ],
}

getNumberOfRows = 50
pages = math.ceil(totalData / getNumberOfRows)

links = {}
lnks = []
for page in range(1, pages+1):

    print(f'Page" {page}, requests done!!')
    response = requests.post(
        f'https://book.myagentgenie.com/nitroapi/v2/cruise?&sortColumn=cruiselinePriority&sortOrder=asc&pageStart={page}&includeFacets=uniqueId&pageSize={getNumberOfRows}&fetchFacets=true&groupByItineraryId=true&applyExchangeRates=true&ignoreCruiseTaxInclusivePref=true&requestSource=1',
        headers=headers,
        cookies=cookies,
        json=json_data,
    )

    data = json.loads(response.content)
    listOfData = data['data']['list']
    for rowData in listOfData:
        linkID = rowData['packages'][0]['id']
        link = f'https://book.myagentgenie.com/swift/cruise/package/{linkID}?siid={carnivalCruiseLineID}&lang=1'
        lnks.append(link)
        
links['url'] = lnks

file = open('newLinks.json', 'w', encoding='utf-8')
json.dump(links, file, ensure_ascii=False)