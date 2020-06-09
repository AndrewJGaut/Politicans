import selenium
from selenium import webdriver


def getDriver():
    '''

    :return: A selenium driver object that can be used for web scraping
    '''
    # define selenium driver for scraping
    options = selenium.webdriver.chrome.options.Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)

    return driver


def convertPartyAfilliation(party):
    '''

    :param party: D, R, or I
    :return: democrat, repulican, or independent (respectively)
    '''
    if party == 'D':
        return 'democrat'
    elif party == 'R':
        return 'republican'
    elif party == 'I':
        return 'independent'
    else:
        raise Exception("We don't have support for this party affiliation.")