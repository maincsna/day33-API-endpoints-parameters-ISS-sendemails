import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 37.368832
MY_LONG = -122.036346

#create email and password
my_email = "manafreedom@gmail.com"
my_password = "deptazfajupzldvx"

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    # if response.status_code == 404:
    #     raise Exception("That resource does not exist.")
    # elif response.status_code == 401:
    #     raise Exception("You are not authorized to access this data")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the iss position.
    if (MY_LAT-5 <= iss_latitude <= MY_LAT+5 and
        MY_LONG -5 <= iss_longitude <= MY_LONG+5):
        return True

def is_night():
    parameters ={
        "lat": MY_LAT,
        "lng":MY_LONG,
        "formatted":0
    }

    response = requests.get("http://api.sunrise-sunset.org/json",params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    print(time_now.hour)

    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(my_email,my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject:Look up \n\n The ISS is above you in the sky."
        )

