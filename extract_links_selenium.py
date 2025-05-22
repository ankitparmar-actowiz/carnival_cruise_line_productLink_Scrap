from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from undetected_chromedriver import Chrome
from selenium.webdriver.common.by import By
import time, pyperclip, json

driver = Chrome()

driver.get('https://tap5.myagentgenie.com/phillipcrane/')
driver.maximize_window()
time.sleep(5)

while True:
    try:
        isDataLoad = driver.find_element(By.XPATH, '//div[@class="multiselect__tags"]')
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

urls = {}
links = []
diff = 0
for data in range(1, totalData+1):

    totalItineriesCount = len(driver.find_elements(By.XPATH, '//*[@data-ody-id="CruiseInfoCardWrapper"]'))

    if totalItineriesCount == data:

        clickShare = driver.find_element(By.XPATH, f'((//div[@data-ody-id="CruiseInfoCardWrapper"])[last()]//em[@class="odi odi-share"]/parent::button[1])[1]')
        driver.execute_script('arguments[0].click();', clickShare)
        time.sleep(1)

        url = pyperclip.paste()
        links.append(url)

    elif ((data+diff) % 10) == 0:
        diff += 1

        viewMore = driver.find_element(By.XPATH, '//button[contains(@class, "btn-view-more")]')
        driver.execute_script('arguments[0].click();', viewMore)
        time.sleep(1)

        while True:
            try:
                newtotalItineriesCount = len(driver.find_elements(By.XPATH, '//*[@data-ody-id="CruiseInfoCardWrapper"]'))
            except:
                newtotalItineriesCount = None
            if newtotalItineriesCount == data:
                break
            else:
                print('.', end='')
                time.sleep(1)
        time.sleep(1)
        
        clickShare = driver.find_element(By.XPATH, f'((//div[@data-ody-id="CruiseInfoCardWrapper"])[last()]//em[@class="odi odi-share"]/parent::button[1])[1]')
        driver.execute_script('arguments[0].click();', clickShare)
        time.sleep(1)

        url = pyperclip.paste()
        links.append(url)
    else:
        print('breaked!!')
        exit()

    driver.back()

    actions.send_keys(Keys.END).perform()
    time.sleep(1)

urls['urls'] = links
driver.quit()
file = open('links_paste.json', 'w', encoding='utf-8')
json.dump(urls, file, ensure_ascii=False)
print('Completed')