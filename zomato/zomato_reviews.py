from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.zomato.com/chennai/paradise-perungudi/reviews")
link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Load More")))
ActionChains(browser).move_to_element(link).perform()
link.click()