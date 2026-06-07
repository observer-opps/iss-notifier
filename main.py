import requests
import math
import smtplib
import time

# your coordinates — replace with your actual latitude and longitude
my_lat = 100.00000
my_lon = 50.00000

# gmail smtp server config
smtp_host = "smtp.gmail.com"
smtp_port = 587

# email credentials — replace with your actual values
sender_email = "sender@gmail.com"
receiver_email = "receiver@gmail.com"
password = "yourapppassword"
message = "ISS IS ABOVE YOU"

# ISS location API endpoint
iss_api = "https://api.wheretheiss.at/v1/satellites/25544"


def send_email(sender_email, receiver_email, password, message, smtp_host, smtp_port):
    # connect to gmail, upgrade to encrypted connection, login, send
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def haversine_formula(my_lat, my_lon, iss_lat, iss_lon):
    # convert all coordinates from degrees to radians
    iss_lat = math.radians(iss_lat)
    iss_lon = math.radians(iss_lon)
    my_lat = math.radians(my_lat)
    my_lon = math.radians(my_lon)

    # angular differences between the two points
    d_lat = iss_lat - my_lat
    d_lon = iss_lon - my_lon

    # haversine formula — returns distance in km between two points on a sphere
    a = math.sin(d_lat/2)**2 + math.cos(my_lat) * math.cos(iss_lat) * math.sin(d_lon/2)**2
    b = math.asin(math.sqrt(a))
    c = 2 * 6371 * b  # 6371 is Earth's radius in km
    return c


# flag to avoid sending repeated emails during the same pass
email_sent = False

while True:
    # fetch current ISS position
    response = requests.get(iss_api)
    data = response.json()

    iss_lon = data["longitude"]
    iss_lat = data["latitude"]

    # calculate distance between you and the ISS ground track
    distance = haversine_formula(my_lat, my_lon, iss_lat, iss_lon)

    # send email only once per pass (when ISS enters 1000km range)
    if distance < 1000 and email_sent == False:
        send_email(sender_email, receiver_email, password, message, smtp_host, smtp_port)
        email_sent = True

    # reset flag once ISS moves out of range
    if distance >= 1000:
        email_sent = False

    # wait 60 seconds before checking again
    time.sleep(60)
