from selenium import webdriver
from selenium.webdriver.common.by import By



# Create a WebDriver instance using Chrome
driver = webdriver.Chrome()

# Get the page
driver.get("http://localhost/calculator.html")

visitor_name = driver.find_element(By.NAME, "visitor_name").send_keys("<script>window.location.href='https://owasp.org/www-community/attacks/xss/'</script>")
number1 = driver.find_element(By.NAME, "number1").send_keys('1')
number2 = driver.find_element(By.NAME, "number2").send_keys('2')


# Submit the form
driver.find_element(By.ID, 'submit_button').submit()

# Get the page source
page_source = driver.page_source

# Print the page source
print(page_source)

# Quit the web driver
driver.quit()

