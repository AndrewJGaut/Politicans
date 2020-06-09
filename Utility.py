import selenium



def getBrowser():
    '''

    :return: A selenium browser object that can be used for web scraping
    '''
    # define selenium browser for scraping
    options = selenium.webdriver.chrome.options.Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    browser = selenium.webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)

    return browser