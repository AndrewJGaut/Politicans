from Utility import *
import pprint




def getSenatorVotesForOneBill(driver):
    '''
    @param: driver: the driver object being used to scrape stuff; note that this should ALREADY be on the
    page in question! (the page with the votes)
    @param bill: the bill in question (this only gets votes for one bill)
    :return: A dictionary of the form
        {
            'Johnson': {
                'party': 'Democrat',
                'vote': 'Yea',
                'state': 'CA'
            },
            ...
        }
    '''


    def processVotes(votes_string):
        '''

        :param votes_string: a string of votes in the format:
         Johnson (D-TN), Yea
         Smith (R-CA), Nay
        :return: A dictionary of the form
        {
            'Johnson': {
                'party': 'Democrat',
                'vote': 'Yea',
                'state': 'CA'
            },
            ...
        }
        '''
        votes_per_politician = votes_string.split("\n")

        data = dict()
        for vote_per_politican in votes_per_politician:
            meta_info, vote = vote_per_politican.split(',')

            vote = vote.strip()

            test = meta_info.split()

            last_name, other_info = meta_info.split('(')

            last_name = last_name.strip()

            party_affiliation, state = other_info.split('-')
            party_affiliation = convertPartyAfilliation(party_affiliation)
            state = state[:-1]


            '''NOTE!!!!!: WE NEED TO MAKE SURE NONE HAVE THE SAME LAST NAME OR ELSE FIND A WAY
            TO FIND THEIR FULL NAME BEFORE DOING THIS STEP!'''
            data[last_name] = {'party': party_affiliation, 'last name': last_name, 'state': state, 'vote': vote}

        return data



    # get the relevant span elements
    span_elements = driver.find_elements_by_css_selector("span[class='contenttext']")

    # make sure we got an element back
    assert(len(span_elements) > 0)

    # the first element will give us the FULL list of senator names and their votes
    span_element = span_elements[0]
    votes = span_element.text

    # process the votes
    processed_votes = processVotes(votes)
    return processed_votes


def getVotesForAllBillsForOneYear(driver):
    '''

    :param driver: chromedriver that should ALREADY be on the page listing the bills
    :return:
    '''

    table = driver.find_element_by_id('listOfVotes')

    for table_row in table.find_elements_by_tag_name('tr'):
        # get all the td elements

        # for each row, we first want to check if this row represents a bill vote.


        # next, we'll get the bill name and URL

        # get the votes by clicking on the link, calling function, and stepping back to the current page
        driver.get('url')
        processed_votes_for_bill = getSenatorVotesForOneBill(driver)
        driver.back()

        # update the dictionary object












driver = getDriver()
#driver.get("https://www.senate.gov/legislative/LIS/roll_call_lists/roll_call_vote_cfm.cfm?congress=116&session=2&vote=00114")
driver.get("file:///Users/agaut/PycharmProjects/Politicans/HtmlFilesForTesting/senate_names.html")
getSenatorVotesForOneBill(driver)

pp = pprint.PrettyPrinter(width=41, compact=True)


'''
<tr>
<td valign="top" class="contenttext">
    <span style="display:none">(00113) </span>
    <a href="/legislative/LIS/roll_call_lists/roll_call_vote_cfm.cfm?congress=116&amp;session=2&amp;vote=00113">113&nbsp;(53-38)</a>
</td>
<td valign="top" class="contenttext">
    Confirmed
</td>
<td valign="top" class="contenttext">
    On the Nomination: Confirmation: Michael Pack, of Maryland, to be Chief Executive Officer of the Broadcasting Board of Governors
</td>
<td valign="top" class="contenttext">
    <a href="https://www.congress.gov/nomination/116th-congress/1590">PN1590</a>
</td>
<td valign="top" class="contenttext">
    Jun&nbsp;04
</td>
</tr>


example name of bill: H.R. 1957
'''