#IMPORTING LIBRARIES
import requests
from bs4 import BeautifulSoup
import time
from smtplib import SMTP
import ssl

#SENDER EMAIL
senderemail = 'shivangi6002@gmail.com'

#USER DETAILS
#Product URL
link = "https://www.amazon.in/dp/B079GV1M9Z/"
#User E-Mail
email = 'youremail@gmail.com'
#User E-Mail App Password (Can be genereated from Google Account settings)
password = 'xxxxxx'
#Maximum Affordable Price to check price drop
max_allowed_price = 9000.0

#Sending request to fetch HTML of the page
r = requests.get(link, headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"})
c = r.content
# Creating soup object
soup = BeautifulSoup(c, "html.parser")

#FUNCTION that check whether the product is in Deal Price. If not, then checks whether there is price drop in regular price.
def check_price():
    try:
      ProductName = soup.find(id= "productTitle").get_text()
      price = soup.find(id = 'priceblock_dealprice')
      price_type = "at Deal Price"
      price = ((price.get_text()).strip())
      pricetemp = list(price)
      pricetemp = [i.replace(',','') for i in pricetemp]
      price = ''.join(pricetemp)
      price = float(price[1:])
      notify(ProductName,price, price_type)
    except AttributeError:
      ProductName = soup.find(id= "productTitle").get_text()
      price = soup.find(id = 'priceblock_ourprice')
      price_type = "on a lower price"
      price = ((price.get_text()).strip())
      pricetemp = list(price)
      pricetemp = [i.replace(',','') for i in pricetemp]
      price = ''.join(pricetemp)
      price = float(price[1:])
      if (price <= max_allowed_price):
        notify(ProductName,price, price_type)

#FUNCTION that sends an E-mail to the user 
def notify(ProductName, price, price_type):
  SMTP_server = 'smtp.gmail.com'
  port = 587
  server = SMTP(SMTP_server, port)
  server.starttls()
  server.login(email, password)
  subject = f"{ProductName} is available {price_type}!"
  body = f"{ProductName} is now available at Rs. {price}. Check the amazon link {link}"
  message = f"Subject: {subject}\n\n{body}"
  server.sendmail(senderemail, email, message)
  print('The E-mail has been sent')
  server.quit()

#LOOP that allows the program to check everyday (every 24 hours) of Continuous System Up Time.
while(True):
  check_price()
  time.sleep(60*60*24)