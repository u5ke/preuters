from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs
from bs4 import BeautifulSoup
import re
from flask import Flask, request
import urllib.parse

app = Flask(__name__)


@app.route("/")
def index():

    CHROMEDRIVER = '/opt/chrome/chromedriver'
    # URL = 'https://www.reuters.com/site-search/?query=Space+operations&sort=oldest&offset=20'
    # app.logger.debug(request.args.to_dict())

    URL2 = urllib.parse.urlencode(request.args.to_dict())
    # app.logger.debug(URL2)
    URL3 = urllib.parse.unquote(URL2)[2:]
    # app.logger.debug(URL3)
    URL = URL3

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    chrome_service = fs.Service(executable_path=CHROMEDRIVER)
    driver = webdriver.Chrome(service=chrome_service, options=options)
    driver.get(URL)
    r = BeautifulSoup(driver.page_source, "lxml")
    for atag in r.find_all('a'):
        if re.fullmatch(r'/.+[12][0-9][0-9][0-9]-[01][0-9]-[0-3][0-9]/', atag.get('href')) is not None:
            print('match ' + atag.get('href'))
            atag.attrs['href'] = 'https://www.reuters.com' + atag.attrs['href']
        else:
            print('delete ' + atag.get('href'))
            del atag.attrs['href']

    # print('-------------------------')
    # print(r)
    return str(r)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
