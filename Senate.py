from Utility import *




def getSenatorVotesForOneBill(browser, bill):
    '''
    @param: browser: the browser object being used to scrape stuff; note that this should ALREADY be on the
    page in question! (the page with the votes)
    @param bill: the bill in question (this only gets votes for one bill)
    :return: A dictionary mapping senator name --> their vote on the bill in question
    '''

    SPAN_TEXT_FOR_VOTES = 'Alphabetical by Senator Name'
    span_element = browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(SPAN_TEXT_FOR_VOTES))

    assert(len(span_element) == 1) # there should only be ONE such element
    span_element = span_element[0] # as long as there is only 1, we can safely convert the variable to a non-list


    # now, get the votes from within the span element