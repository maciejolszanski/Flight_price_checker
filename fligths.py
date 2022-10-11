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


if __name__ == "__main__":

    driver = webdriver.Edge()
    # driver.implicitly_wait(3)
    driver.get(SKYSCANNER_BASE_URL)

    # accepting cookies
    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button').click()

    # filling destination, at first we need to click the field, and then select
    # the field taht is enlarged - has different XPATH
    driver.find_element(By.XPATH, '//*[@id="i14"]/div[4]/div/div/div[1]/div/div/input').click()
    destination_form = driver.find_element(By.XPATH, '//*[@id="i14"]/div[6]/div[2]/div[2]/div[1]/div/input')
    destination_form.clear()
    destination_form.send_keys("Barcelona", Keys.ENTER)

    # departure date form                          
    dep_date_form = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input')
    dep_date_form.clear()                          
    dep_date_form.send_keys("2023.02.03", Keys.ENTER)

    # return date form 
    ret_date_form = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div/input')
    ret_date_form.clear()
    ret_date_form.send_keys("2023.02.06", Keys.ENTER)
