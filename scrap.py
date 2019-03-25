import pandas as pd
from splinter import Browser
"""This scrapper was created by montegry, with help of habr.com. It using chrome driver and splinter lib."""
browser = Browser('chrome') # create a Browser
browser.driver.set_window_size(640, 480)
browser.visit("https://www.google.com") # Let the Browser visit google page
search_bar_xpath = '//*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input' # initialize search bar by xpath (copy form Chrome )
search_bar = browser.find_by_xpath(search_bar_xpath)[0]
button_xpath = '//*[@id="tsf"]/div[2]/div/div[2]/div[2]/div/center/input[1]' # initialize search button 
button = browser.find_by_xpath(button_xpath)[0]
search_bar.fill('Hello, world!') # filling searchbar with request
button.click() # click the search button
find_xpath = '//div[@class="r"]' # finding all html tags with div class r
search_results = browser.find_by_xpath(find_xpath)
scraped_data = []
for search_result in search_results:
     title = search_result.text # trust me
     link = search_result.html
     scraped_data.append((title, link))  # put in tuples
df = pd.DataFrame(data=scraped_data, columns=['Title', 'Href']) # creating dataframe to write it in csv next
df.to_csv("Data.csv")
browser.quit()
