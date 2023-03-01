## Webscraper that returns the latest x items posted on the furniture website

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# TODELETE: Global variable
desired_quantity = 0

# TODELETE: Data class
class User:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

class Scraper:
    def __init__(self, options) -> None:
        self.options = options
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

    # TO DELETE: Use filter instead  of loop
    def find_digit(self, string):
        output = ''
        for i in string:
            if i.isdigit():
                output = output + i
        return output

    # TODELETE: Lazy class or element
    # TODELETE: Feature envy
    def getTags(self, user):
        return [user.usernameTag, user.passwordTag]

    def login(self, url, username, password, usernameTag, passwordTag):
        #Log in
        self.driver.get(url)
        self.driver.find_element("name", usernameTag).send_keys(username)
        self.driver.find_element("name", passwordTag).send_keys(password)
        self.driver.find_element("xpath", '//button[@type="submit"]').click()

    # TODELETE: Long param list
    def getInfoFromSite(self, username, password, url, desiredquantity):
        htmlTags = self.getTags()
        self.login(username, url, password, htmlTags[0], htmlTags[1])

        # Get list
        count_element = self.driver.find_element("xpath", '//p[@class="woocommerce-result-count"]').text

        count = self.find_digit(count_element) # Extract count
        print("There are", int(count), "items and the top ", desiredquantity, "are desired")

        # Get new item
        items_list = self.driver.find_element("xpath", '//ul[@class="products columns-5"]') 
        items_list = items_list.get_attribute("innerHTML") # Get list of postings in html format
        soup = BeautifulSoup(items_list, 'html.parser') # Create soup object for easy parsing
        items = soup.find_all('li') # Get array of items on nettbutikk
        return items[:desired_quantity]
        '''
        latest_item = items[0]
        latest_item_name = latest_item.find('h2').get_text()
        latest_item_link = latest_item.find('a').get('href')
        print("link to",latest_item_name, ":", latest_item_link)
        '''
    
# Main code    
options = Options()
options.add_argument("--headless=new")
scraper = Scraper(options)
user1 = User("testuser", "testpass")
listOfItems = scraper.getInfoFromSite(user1.username, user1.password, "https://www.ntnu.no/nettbutikk/gjenbruk/produktkategori/produkter/", desired_quantity)