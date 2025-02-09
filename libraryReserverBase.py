from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import datetime
import pickle

#Change this definition to match your desired day of week and time
def get_next_wednesday_at_1130():
    today = datetime.date.today()
    days_ahead = (2 - today.weekday() + 7) % 7 
    if days_ahead == 0:
        days_ahead = 7 
    next_wednesday = today + datetime.timedelta(days_ahead)
    return datetime.datetime.combine(next_wednesday, datetime.time(11, 30))

next_wednesday_1130 = get_next_wednesday_at_1130()
formatted_date_time = next_wednesday_1130.strftime("%I:%M%p %A, %B %d, %Y").lower()
formatted_date_time = formatted_date_time.replace("am", "am ").replace("pm", "pm ")  
formatted_date_time = formatted_date_time.replace(" 0", " ") 
formatted_date_time = ' '.join(word.capitalize() for word in formatted_date_time.split())  
formatted_date_time = formatted_date_time.replace('Am ', 'am ').replace('Pm ', 'pm ')  

print("Formatted datetime for selection:", formatted_date_time)

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://vcu.libcal.com/spaces?lid=16885&gid=35721&c=0")

wait = WebDriverWait(driver, 10)
dropdown_element = wait.until(EC.visibility_of_element_located((By.ID, 'gid')))
dropdown = Select(dropdown_element)
dropdown.select_by_value('36707')

go_to_date_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-goToDate-button")))
go_to_date_button.click()

todaysDate = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'today.day')))

next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.fc-next-button.btn.btn-default.btn-sm')))
next_button.click()

#Replace "Timeslot" with your desired time (ex: "9:30am Wednesday"), "Room Number" with your desired room number (ex: 301e)
time_slot_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@aria-label, 'Timeslot') and contains(@aria-label, 'Room Number') and contains(@aria-label, 'Available')]")))
time_slot_element.click()

lengthDropdown_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//select[contains(@id, 'bookingend_')]")))
lengthDropdown = Select(lengthDropdown_element)
lengthDropdown.select_by_visible_text(formatted_date_time)

submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit_times')))
submit_button.click()

time.sleep(3)
username_input = driver.find_element(By.ID, "username")
#Replace with actual username
username_input.send_keys("username!") 

password_input = driver.find_element(By.ID, "password")
#Replace with actual password
password_input.send_keys("password!")
login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()


cookies = driver.get_cookies()
with open("cookies.pkl", "wb") as file:
    pickle.dump(cookies, file)

time.sleep(15)

submit_booking_button = driver.find_element(By.ID, 'btn-form-submit')
submit_booking_button.click()

time.sleep(10)
driver.quit()
