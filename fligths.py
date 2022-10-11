import re
import datetime
import json

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


DEPART_LATEST = datetime.date(2023, 2, 3)
RETURN_EARLIEST = datetime.date(2023, 2, 6)
DESTINATION = "Barcelona"
SKYSCANNER_BASE_URL = f"https://www.google.com/travel/flights"



def format_date(date):

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
    dep_date_form.send_keys(format_date(dep_date), Keys.ENTER)

    # return date form 
    ret_date_form = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div/input')
    ret_date_form.clear()
    ret_date_form.send_keys(format_date(ret_date), Keys.ENTER)

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

    all_results = driver.find_elements(By.CLASS_NAME, 'JMc5Xc')
    print("Number of results: ", len(all_results))

    filename = "flights_data.json"

    with open(filename, 'r') as f:

        file_dict = json.load(f)
        

        for elem in all_results:
            text = elem.get_attribute('aria-label')

            price = re.findall(r"From \d+", text)[0].split(' ')[1]

            nonstop = re.findall(r"\bNon", text)
            if len(nonstop) > 0:
                stops = 0
                stop_time = None
                stop_city = None
            else:
                stops = re.findall(r"\d+ stop", text)[0].split(' ')[0]
                stop_data = re.findall(r'((\d+ hr)? (\d+ min)?)+ (overnight )?layover at (\S+)', text)
                stop_time = stop_data[0][0].strip()
                stop_city = stop_data[0][4].strip()

            airline = ' '.join(re.findall(r"((with \S+) (\S+\.)?)", text)[0][0].split(' ')[1:])
            airline = airline.rstrip()[:-1] # removing dot

            times = re.findall(r"\d+:\d+ [APM]+", text)
            dep_time = times[0]
            arr_time = times[1]

            dates = re.findall(r"\S+, \S+ \d", text)
            dep_date = dates[0] + " 2023"
            arr_date = dates[1] + " 2023"

            duration = (re.findall(r"((duration \d+ hr\.?)+ (\d+ min)?)", text)[0][0])
            duration = ' '.join(duration.split(' ')[1:]).rstrip()
            if duration[-1] == '.':
                duration = duration[:-1]       
            
            today = format_date(datetime.date.today())
            
            elem_dict = {
                "date_readed": today,
                "departure_date": dep_date,
                "arrival_date": arr_date,
                "return_date": format_date(RETURN_EARLIEST),
                "price": int(price),
                "airline": airline,
                "duration": duration,
                "stops": {
                    "stops_num": stops,
                    "place": stop_city,
                    "stop_duration": stop_time,
                }
            }

            file_dict["items"].append(elem_dict)

        driver.close()
    
    with open(filename, 'w') as f:
        print(file_dict)
        json.dump(file_dict, f)


"""
From 608 Polish zlotys round trip total. 
1 stop flight with Lufthansa. 
Leaves John Paul II Kraków-Balice International Airport at 1:25 PM on Friday, February 3 
and arrives at Josep Tarradellas Barcelona-El Prat Airport at 5:35 PM on Friday, February 3.
Total duration 4 hr 10 min. 
Layover (1 of 1) is a 50 min layover at Munich International Airport in Munich. 
Select flight

From 1158 Polish zlotys round trip total.
This price does not include overhead bin access.
Nonstop flight with Wizz Air.
Leaves John Paul II Kraków-Balice International Airport at 6:45 AM on Friday, February 3
and arrives at Josep Tarradellas Barcelona-El Prat Airport at 9:30 AM on Friday, February 3
"""
