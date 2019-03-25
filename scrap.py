import pandas as pd
from splinter import Browser

browser = Browser('chrome')
browser.driver.set_window_size(640, 480)
browser.visit("https://www.google.com")
search_bar_xpath = '//*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input'
search_bar = browser.find_by_xpath(search_bar_xpath)[0]
button_xpath = '//*[@id="tsf"]/div[2]/div/div[2]/div[2]/div/center/input[1]'
button = browser.find_by_xpath(button_xpath)[0]
search_bar.fill('Hello, world!')
button.click()
find_xpath = '//div[@class="r"]'
search_results = browser.find_by_xpath(find_xpath)
scraped_data = []
for search_result in search_results:
     title = search_result.text # trust me
     link = search_result.html
     scraped_data.append((title, link))  # put in tuples
df = pd.DataFrame(data=scraped_data, columns=['Title', 'Href'])
df.to_csv("Data.csv")
browser.quit()
