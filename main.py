import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

textList = []
email = "email@gmail.com"
pas = "password"
sms_gateway = 'phoneNumber@tmomail.net'
smtp = "smtp.gmail.com"
port = 587
checkText = "Thank you for your application. Your file is currently " \
            "complete and under review. A decision has not yet been made on your " \
            "application to Drexel University. If additional materials are required " \
            "before an admission decision can be rendered, we will contact you."
scrapedText = ""
hours = 4

#convert hours to seconds
hours = hours * 60 * 60

def scrapeSite():
    global scrapedText
    global checkText
    global textList

    options = Options()
    options.headless = True
    driver = webdriver.Firefox()
    driver.get("https://discover.drexel.edu/secure/login")
    time.sleep(2)
    userfield = driver.find_elements_by_id('username')[0]
    passfield = driver.find_elements_by_id('password')[0]
    userfield.send_keys('email@gmail.com')
    passfield.send_keys('password')
    time.sleep(1)
    passfield.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.get("https://admissions.drexel.edu/apply/status")
    time.sleep(2)
    data = driver.find_elements_by_tag_name('p')

    for item in data:
        textList.append(item.text)

    scrapedText = textList[1]
    driver.quit()

    if scrapedText == checkText:
        sendNoChangeMessage()
    else:
        sendChangeMessage()

def sendNoChangeMessage():
    # This will start our email server
    server = smtplib.SMTP(smtp,port)
    # Starting the server
    server.starttls()
    # Now we need to login
    server.login(email,pas)
    # Now we use the MIME module to structure our message.
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = sms_gateway
    # Make sure you add a new line in the subject
    msg['Subject'] = "Drexel Admission" + "\n"
    # Make sure you also add new lines to your body
    body = "No word back yet..." + "\n"
    # and then attach that body furthermore you can also send html content.
    msg.attach(MIMEText(body, 'plain'))
    sms = msg.as_string()
    server.sendmail(email,sms_gateway,sms)
    # lastly quit the server
    server.quit()

def sendChangeMessage():
    # This will start our email server
    server = smtplib.SMTP(smtp,port)
    # Starting the server
    server.starttls()
    # Now we need to login
    server.login(email,pas)
    # Now we use the MIME module to structure our message.
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = sms_gateway
    # Make sure you add a new line in the subject
    msg['Subject'] = "Drexel Admission" + "\n"
    # Make sure you also add new lines to your body
    body = "Something changed homie, go log in and see if you were " \
           "accepted." + "\n"
    # and then attach that body furthermore you can also send html content.
    msg.attach(MIMEText(body, 'plain'))
    sms = msg.as_string()
    server.sendmail(email,sms_gateway,sms)
    # lastly quit the server
    server.quit()


def repeater():
    global hours
    scrapeSite()
    time.sleep(hours)

while True:
    repeater()
