from selenium import webdriver

# Specify the executable directly since it's in the same directory
driver = webdriver.Chrome('./chromedriver-linux64/chromedriver')

# Navigate to a webpage
driver.get('https://www.python.org')

# Example action: print the title of the page
print(driver.title)

# Quit the driver to close the browser
driver.quit()
