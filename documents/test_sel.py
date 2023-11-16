from selenium import webdriver

# Create a WebDriver instance using Chrome
driver = webdriver.Chrome()

# Get the page
driver.get("https://www.python.org")

# Don't forget to quit the WebDriver when you're done
driver.quit()

