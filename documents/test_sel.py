from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up the service object to point to where the chromedriver executable is located
service = Service(executable_path='./chromedriver-linux64/chromedriver')


# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=service)


# Navigate to a webpage
driver.get('https://www.python.org')

# Example action: print the title of the page
print(driver.title)

# Quit the driver to close the browser
driver.quit()
