import re
import datetime
import json

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


DEPART_EARLIEST = datetime.date(2023, 2, 2)
DEPART_LATEST = datetime.date(2023, 2, 3)
RETURN_EARLIEST = datetime.date(2023, 2, 6)
RETURN_LASTEST = datetime.date(2023, 2, 8)
DESTINATION = "Barcelona"
SOURCE = "Kraków"
GOOGLE_BASE_URL = f"https://www.google.com/travel/flights"
FILENAME = r"data\flights_data.json"


def format_date(date):

    formatted_date = '.'.join(str(date).split('-'))

    return formatted_date

def find_all_dates(dep_earl, dep_lat, ret_earl, ret_lat):

    dep = dep_earl
    ret = ret_earl

    dates_list = []

    while dep <= dep_lat:
        while ret <= ret_lat:

            dates = (dep, ret)
            dates_list.append(dates)
            ret += datetime.timedelta(days=1)

        ret = ret_earl
        dep += datetime.timedelta(days=1)

    return dates_list

def input_destination(source, dest):

    # filling source and destination, at first we need to click the field, and then select
    # the field that is enlarged - has different XPATH

    driver.find_element(By.XPATH, '//*[@id="i14"]/div[1]/div/div/div[1]/div/div/input').click()
    source_form = driver.find_element(By.XPATH, '//*[@id="i14"]/div[6]/div[2]/div[2]/div[1]/div/input')
    source_form.clear()
    source_form.send_keys(source, Keys.ENTER)

    driver.find_element(By.XPATH, '//*[@id="i14"]/div[4]/div/div/div[1]/div/div/input').click()
    destination_form = driver.find_element(By.XPATH, '//*[@id="i14"]/div[6]/div[2]/div[2]/div[1]/div/input')
    destination_form.clear()
    destination_form.send_keys(dest, Keys.ENTER)

    sleep(1)

def input_dates(dep_date, ret_date):

    # departure date form                          
    dep_date_form = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input')
    dep_date_form.clear()                          
    dep_date_form.send_keys(format_date(dep_date), Keys.ENTER)

    # return date form 
    ret_date_form = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div/input')
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

def get_stops_data(text):

    single_stops_list = []
    nonstop = re.findall(r"\bNon", text)
    
    if len(nonstop) > 0:
        stops = 0
        stop_time = None
        stop_city = None
    else:
        stops = re.findall(r"\d+ stop", text)[0].split(' ')[0]
        stop_data = re.findall(r'((\d+ hr\s?)?(\d+ min)?)+ (overnight )?layover at (\S+)', text)

        for i, stop in enumerate(stop_data):
            stop_time =  stop[1].lstrip() + stop[2].strip()
            stop_city = stop[4].strip()

            single_stop_dict = {
                "stop_num": i+1,
                "duration": stop_time,
                "place": stop_city
            }

            single_stops_list.append(single_stop_dict)

    stops_dict = {
        "stops": int(stops),
        "stops_data": single_stops_list
    } 

    return stops_dict

def get_flight_data(elem, ret_date):

    try: text = elem.get_attribute('aria-label')
    except Exception as err: 
        print('Handling run-time error:', err)
        return None, False

    price = re.findall(r"From \d+", text)[0].split(' ')[1]

    stops_data = get_stops_data(text)

    airlines = re.findall(r"(with ([a-zA-Z ]+\.))", text)[0][-1].strip()[:-1]
    airlines = airlines.split(' and ')

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
        "departure_time": dep_time,
        "arrival_time": arr_time,
        "return_date": format_date(ret_date),
        "price": int(price),
        "airline": airlines,
        "duration": duration,
        "stops": stops_data
    }

    return elem_dict, True


if __name__ == "__main__":

    driver = webdriver.Edge()
    driver.implicitly_wait(3)
    driver.get(GOOGLE_BASE_URL)

    # accepting cookies
    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button').click()

    source = SOURCE
    dest = DESTINATION
    input_destination(source, dest)

    # search
    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button').click()

    dates = find_all_dates(DEPART_EARLIEST, DEPART_LATEST, RETURN_EARLIEST, RETURN_LASTEST)

    errors = 0

    with open(FILENAME, 'r') as f:

        file_dict = json.load(f)

    for (dep_date, ret_date) in dates:
        input_dates(dep_date, ret_date)

        all_results = driver.find_elements(By.CLASS_NAME, 'JMc5Xc')

        for elem in all_results:

            elem_dict, do_append = get_flight_data(elem, ret_date)

            if do_append:
                file_dict["items"].append(elem_dict)
            else:
                errors += 1

    driver.close()
    print("\nWeb Scraping: SUCCEEDED")
    print(f"Unable to read {errors} flights data")

    with open(FILENAME, 'w') as f:
        json.dump(file_dict, f, indent=4)
        print("Writing Data to File: SUCCEEDED\n")
