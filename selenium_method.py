from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Initialise driver
options = Options()
#options.add_experimental_option("detach", True)
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

# Log in
username = ""
password = ""

driver.get("https://www.ntnu.no/nettbutikk/gjenbruk/produktkategori/produkter/")
driver.find_element("name", "feidename").send_keys(username)
driver.find_element("name", "password").send_keys(password)
driver.find_element("xpath", '//button[@type="submit"]').click()

# Get list
count_element = driver.find_element("xpath", '//p[@class="woocommerce-result-count"]').text
count = ''.join(filter(str.isdigit, count_element)) # Extract count
print("There are", int(count), "items")

# Get new item
items_list = driver.find_element("xpath", '//ul[@class="products columns-5"]') 
items_list = items_list.get_attribute("innerHTML") # Get list of postings in html format
soup = BeautifulSoup(items_list, 'html.parser') # Create soup object for easy parsing
items = soup.find_all('li') # Get array of items on nettbutikk
latest_item = items[0]
latest_item_name = latest_item.find('h2').get_text()
latest_item_link = latest_item.find('a').get('href')
print("link to",latest_item_name, ":", latest_item_link)

# Close web driver
driver.quit()