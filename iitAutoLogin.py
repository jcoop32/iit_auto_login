from selenium import webdriver
from selenium.webdriver.common.by import By

# from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# from selenium.webdriver.chrome.options import Options
from email.message import EmailMessage
import smtplib
import time
import yaml

pathToYaml = "/Users/joshcooper/iit_auto_login/loginDetails.yml"
conf = yaml.full_load(open(pathToYaml))
# iit creds
iit_username = conf["iit_login"]["username"]
iit_password = conf["iit_login"]["password"]
iit_security_question = conf["iit_login"]["sec_ques"]
# email creds
sender_email = conf["bot_email"]["email"]
receiver_email = "jcoopbbb@gmail.com"
subject1 = "New Room available check quickly!"
subject2 = "Update on rooms"
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587  # Use 465 if using SSL
username = conf["bot_email"]["email"]
password = conf["bot_email"]["password"]
image_path = "./rooms.png"
update_image_path = "./updateOfRooms.png"


# service = Service(executable_path="/Users/joshcooper/iit_housing_portal/chromedriver")
options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
# driver = webdriver.Chrome(options=options)
# driver = webdriver.Firefox()

max_time = 1000


def loginPortal(url, limit):
    driver.get(url)
    time.sleep(3)
    driver.find_element(by=By.ID, value="input28").send_keys(iit_username)
    print("Username added")
    driver.find_element(by=By.ID, value="input36").send_keys(iit_password)
    print("password added")
    driver.find_element(by=By.CLASS_NAME, value="button").click()
    print("button clicked")
    time.sleep(3)
    elementsOnSecurityPage = driver.find_elements(By.LINK_TEXT, value="Select")
    elementsOnSecurityPage[1].click()
    print("clicked security question")
    time.sleep(3)
    driver.find_element(By.ID, "input88").send_keys(iit_security_question)
    print("security question added")
    driver.find_element(by=By.CLASS_NAME, value="button").click()
    print("security question submit button clicked")
    time.sleep(5)

    goToApplication(driver, limit)


def goToApplication(driver, limit):
    print("going to application page")
    driver.get(
        "https://iit.okta.com/home/iit_starrezportal_1/0oa3dtq5j5Z1mAJCe697/aln3dtyaphntvPXUV697"
    )
    print("on application page")
    menu = driver.find_element(by=By.LINK_TEXT, value="Academic Year Housing")
    menu.click()
    print("clicked housing application")
    time.sleep(3)
    driver.find_element(by=By.CLASS_NAME, value="sr_button").click()
    print("continue to application btn clicked")
    goToRoomSelecionPage(driver, limit)


def goToRoomSelecionPage(driver, limit):
    time.sleep(3)
    driver.get(
        "https://iit.starrezhousing.com/StarRezPortalX/3B393650/8/16/Academic_Year_Housin-Room_Selection?UrlToken=635D08E0&DateStart=2024-08-12T00%3A00%3A00.000&DateEnd=2025-05-11T00%3A00%3A00.000&LowerRoomRateValue=0&UpperRoomRateValue=0&RoomTypeID=23%2C25%2C26%2C27&ClassificationID=5&TermID=18"
    )
    print("clicked room selection")
    print(driver.current_url)
    print("Filtered Rooms")
    time.sleep(1)
    driver.find_element(by=By.CLASS_NAME, value="cc-dismiss").click()
    print("STARTING REFRESH PHASE...")
    for x in range(0, limit):
        countdown(int(60))
        rooms = driver.find_elements(by=By.CLASS_NAME, value="image-container")
        if len(rooms) > 0:
            driver.save_full_page_screenshot("rooms.png")
            print("getting a screenshot of rooms...")
            time.sleep(1)
            sendRoomNotification()
            print("sent email alert")
        if x % 100 == 0:
            driver.save_full_page_screenshot("updateOfRooms.png")
            print("getting a screenshot for update...")
            time.sleep(1)
            sendUpdateNotification()
            print("sent update email")
        print("refreshing...")
        driver.refresh()
        print("refreshed")
        x += 1
        print("refresh " + str(x))


def sendRoomNotification():
    # Create the email message
    email_message = EmailMessage()
    email_message["From"] = sender_email
    email_message["To"] = receiver_email
    email_message["Subject"] = subject1
    # Attach the message body
    # add image to email
    with open(image_path, "rb") as img:
        img_data = img.read()
    email_message.add_attachment(img_data, maintype="image", subtype="png")
    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Log in to the email account
        server.starttls()  # Use if your server requires a secure connection
        server.login(username, password)
        # Send the email
        server.sendmail(sender_email, receiver_email, email_message.as_string())


def sendUpdateNotification():
    # Create the email message
    email_message = EmailMessage()
    email_message["From"] = sender_email
    email_message["To"] = receiver_email
    email_message["Subject"] = subject2
    # Attach the message body
    # add image to email
    with open(update_image_path, "rb") as img:
        img_data = img.read()
    email_message.add_attachment(img_data, maintype="image", subtype="png")
    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Log in to the email account
        server.starttls()  # Use if your server requires a secure connection
        server.login(username, password)
        # Send the email
        server.sendmail(sender_email, receiver_email, email_message.as_string())


# define the countdown func.
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
        if t == 0:
            break


loginPortal(
    "https://iit.okta.com/oauth2/v1/authorize?client_id=okta.2b1959c8-bcc0-56eb-a589-cfcfb7422f26&code_challenge=Rohl5ay6NZIRZEeTX9advdLQc7PbtgXt1EFfxibDZP4&code_challenge_method=S256&nonce=saEpIzWGtQTJDSv4MtSLBIdAC3xIKxUIQG227XLXMEhVFHwYxMle0xEuHctNXhqf&redirect_uri=https%3A%2F%2Fiit.okta.com%2Fenduser%2Fcallback&response_type=code&state=zuwZqpicsTYz3NcLBi5g1o375NyVhEGchtKT6gbq4cznXu0CV2rcfTfT0ARbBcrl&scope=openid%20profile%20email%20okta.users.read.self%20okta.users.manage.self%20okta.internal.enduser.read%20okta.internal.enduser.manage%20okta.enduser.dashboard.read%20okta.enduser.dashboard.manage%20okta.myAccount.sessions.manage",
    max_time,
)
