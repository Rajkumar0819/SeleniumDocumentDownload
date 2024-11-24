#IMPORT EACH_DAY.TXT FILE
#SELENIUM CODE THAT GOES TO INDIAN KANOON... ITERATES THROUGH EACH DAY
#GETS ALL THE DOCUMENTS THAT ARE AVAILABLE AND STORES IT INTO THE DOWNLOADS FOLDER

#basic imports
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException

#creating a list of all the dates
list_days = []

def read_lines_to_list(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                list_days.append(line.strip())
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    return list_days


# using options to make sure the browser is ready
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
options.add_argument("--disable-extensions")  # Disabling extensions
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
options.add_argument("--no-sandbox")  # Bypass OS security model


#creating a driver to access the elements in web
driver = webdriver.Chrome(options=options)


# Actual page functionality 
def page_functionality():

    loop_variable = True

    while loop_variable:
        time.sleep(2)

        # checks if there is "Next" button available so that it can run iteratively
        try : 
            time.sleep(2)
            next_button = driver.find_element(By.LINK_TEXT, "Next")
        except NoSuchElementException:
            loop_variable = False
        

        # scrollin to the bottom to get all the links visible 
        try : 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            links_of_the_page = driver.find_elements(By.CSS_SELECTOR, "div.result div.result_title a")

            
            # extracting the links and storing them in a list
            for each_link_in_page in links_of_the_page:
                # putting it to a new tab 
                link = each_link_in_page.get_attribute('href')
                print(link)
                driver.execute_script(f'window.open("{link}","_blank");')
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[-1])

                # Clicking the get pdf btn
                get_pdf_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "pdfdoc")))
                get_pdf_btn.click()
                time.sleep(2)

                # switching to original tab
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
            next_button.click()

        
        #General Exceptions cases 
        except Exception as e:
            if e == NoSuchElementException:
                print("No elements")
            else:
                print(e)
        

# goes to indian kannon, searches the date and clicks the search button     
def main_page():

    for i in list_days:

        driver.get("https://indiankanoon.org/")
        time.sleep(1)
        input = driver.find_element(By.XPATH, "/html/body/div[2]/form/input[1]")
        input.send_keys(i)
        driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/form[1]/input[2]").click()
        time.sleep(2)

        # this fucntion is where actual downloading of documents will happen
        page_functionality()

        # count will be ierated and saved so that we can monitor at what status is the code is in 
        # also incase of failure we can see the last date and modify the each_day.txt file to start from particular date.
        with open ("count.txt", "a") as f :
            f.write(f'{str(i)}\n')


# summa oru mass kaaga ipdi eluthi irukan 
if __name__ == "__main__":
    file_path = "each_day.txt"
    list_days = read_lines_to_list(file_path)
    main_page()