import requests
import selectorlib
import smtplib, ssl
import os
import dotenv

dotenv.load_dotenv('information.env')

URL = 'http://programmer100.pythonanywhere.com/tours/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    '''Scrape the page source from the URL'''
    response = requests.get(url, headers=HEADERS)
    page_source = response.text
    return page_source


def extract(page_source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(page_source)['tours']
    return value


def send_email(message):
    host = 'smtp.gmail.com'
    port = 465

    username = os.getenv("MY_USERNAME")
    password = os.getenv("MY_PASSWORD")

    receiver = os.getenv("MY_USERNAME")
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print('Email was sent!')


def store(extracted):
    with open('data.txt', 'a') as file:
        file.write(extracted + '\n')


def read(extracted):
    with open('data.txt', 'r') as file:
        return file.read()


if __name__ == '__main__':
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    content = read(extracted)
    if extracted != 'No upcoming tours':
        if extracted not in content:
            store(extracted)
            send_email(message='Hey, new event was found!')
