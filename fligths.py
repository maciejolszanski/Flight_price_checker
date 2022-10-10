import string
from bs4 import BeautifulSoup
import datetime
import requests


DEPART_LATEST = datetime.date(2023, 2, 3)
RETURN_EARLIEST = datetime.date(2023, 2, 6)
DESTINATION = "bcn"
SKYSCANNER_BASE_URL = f"https://www.skyscanner.pl/transport/flights/krk/{DESTINATION}"
ADULTS = 1

def format_date_url(date):

    formatted_date = ''.join(str(date).split('-'))

    return formatted_date


if __name__ == "__main__":

    url = (SKYSCANNER_BASE_URL + format_date_url(DEPART_LATEST) + '/'
           + format_date_url(RETURN_EARLIEST) + '/'
           + "?adultsv2=" + str(ADULTS) + '&'
           + "&cabinclass=economy&childrenv2=&inboundaltsenabled=false&"
           + "outboundaltsenabled=false&"
           + "preferdirects=" + "true"
           )

    flights_site = requests.get(url).text
    flights_html = BeautifulSoup(flights_site, "html.parser")

    print(flights_html)

    "https://www.skyscanner.pl/transport/loty/krk/bcn/221012/221018/"
    "?adultsv2=1&cabinclass=economy&childrenv2=&inboundaltsenabled=false"
    "&outboundaltsenabled=false&preferdirects=false&priceSourceId="
    "&priceTrace=202210091123*I*KRK*BCN*20221012*gtpl*"
    "FR%7C202210091123*I*BCN*KRK*20221018*gtpl*FR&qp_prevCurrency=PLN&"
    "qp_prevPrice=385&qp_prevProvider=ins_month&rtn=1"