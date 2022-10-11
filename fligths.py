from bs4 import BeautifulSoup
import datetime
import requests
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


DEPART_LATEST = datetime.date(2023, 2, 3)
RETURN_EARLIEST = datetime.date(2023, 2, 6)
DESTINATION = "Barcelona"
SKYSCANNER_BASE_URL = f"https://www.google.com/travel/flights"



def format_date_url(date):

    formatted_date = '.'.join(str(date).split('-'))

    return formatted_date

def input_destination(dest):

    # filling destination, at first we need to click the field, and then select
    # the field that is enlarged - has different XPATH
    driver.find_element(By.XPATH, '//*[@id="i14"]/div[4]/div/div/div[1]/div/div/input').click()
    destination_form = driver.find_element(By.XPATH, '//*[@id="i14"]/div[6]/div[2]/div[2]/div[1]/div/input')
    destination_form.clear()
    destination_form.send_keys(dest, Keys.ENTER)

def input_dates(dep_date, ret_date):

    # departure date form                          
    dep_date_form = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input')
    dep_date_form.clear()                          
    dep_date_form.send_keys(format_date_url(dep_date), Keys.ENTER)

    # return date form 
    ret_date_form = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div/input')
    ret_date_form.clear()
    ret_date_form.send_keys(format_date_url(ret_date), Keys.ENTER)

    # Stop is needed, because sometimes the dates are not being updated until the search button is clicked and then the dates are wrong
    sleep(1)

def choose_num_stops(num_stops):
    # Sometimes the ID changes so this does not work always
    
    # open drop down menu
    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div/div[1]/div/button').click()

    if num_stops > 2:
        print("Too many stops selected - looking for 2 stops")
        num_stops = 2
    
    xpath_dicts = {
        0 : '//*[@id="c73"]',
        1 : '//*[@id="c74"]',
        2 : '//*[@id="c75"]',
    }

    # choose number of stops
    driver.find_element(By.XPATH, xpath_dicts[num_stops]).click()

    # close drop down menu
    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div[2]/div[3]/div/div[1]/div[2]/span/button').click()


if __name__ == "__main__":

    driver = webdriver.Edge()
    driver.implicitly_wait(3)
    driver.get(SKYSCANNER_BASE_URL)

    # accepting cookies
    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button').click()

    input_destination(DESTINATION)
    input_dates(DEPART_LATEST, RETURN_EARLIEST)

    # search
    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button').click()
    
    # Sometimes the ID changes so this does not work always
    # choose_num_stops(0)

    all_results = driver.find_elements(By.CLASS_NAME, 'pIav2d')
    print("Number of results: ", len(all_results))
    print(all_results)

