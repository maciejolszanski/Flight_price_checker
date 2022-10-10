from bs4 import BeautifulSoup
import datetime
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


DEPART_LATEST = datetime.date(2023, 2, 3)
RETURN_EARLIEST = datetime.date(2023, 2, 6)
DESTINATION = "bcn"
SKYSCANNER_BASE_URL = f"https://www.skyscanner.pl/transport/flights/krk/{DESTINATION}"



def format_date_url(date):

    formatted_date = ''.join(str(date).split('-'))

    return formatted_date


if __name__ == "__main__":

    flights_site = requests.get(url).text
    flights_html = BeautifulSoup(flights_site, "html.parser")

    print(flights_html)