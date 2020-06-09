from Utility import *
import pprint


class Bill:
    def __init__(self, tally, result, description, issue, date, url):
        self.tally = tally # the total tally of votes on the bill for all senators
        self.result = result # whether or not it was passed
        self.description = description # description of the bill
        self.issue = issue # the name of hte bill
        self.date = date # CHECK ON THIS
        self.url = url # url that gives the offical page of the bill


    @classmethod
    def initFromTableData(cls, table_datas):
        '''

        :param table_data: a list of td elements that MUST be in the order vote, result, description, issue, date
        :return: initializes the object
        '''
        vote = table_datas[0].text
        result = table_datas[1].text
        description = table_datas[2].text
        issue = table_datas[3].text
        date = table_datas[4].text

        url = None
        try:
            url = table_datas[3].find_element_by_tag_name('a').get_attribute('href')
        except:
            print("item with name {} has no relevant url".format(issue))

        return cls(vote, result, description, issue, date, url)

    def __dict__(self):
        # only return the member variables (NOT FUNCTIONS) when printing the dictionary for this object
        # use this override so we can json serialize this object when we write it
        return vars(self)




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




    def getTextForColumn(table_datas, columns, column_name):
        '''
        :param column_name: the name of the column in the table for which we want info
        :return: the text data in the td element under th ecolumn in the table with name column_name
        '''
        return  table_datas[columns.index(column_name)].text

    def isBill(bill):
        '''

        :param bill: a bill object
        :return: whetehr or not this particular table row represents a vote for a bill or not.
        '''

        issue = bill.issue

        for prefix in PREFIXES_FOR_BILLS:
            if prefix in issue:
                return True

        return False






    # these are prefixes for issue names that indicate that the issue is a bill
    PREFIXES_FOR_BILLS = ["H.R."]


    table = driver.find_element_by_id('listOfVotes')



    hrefs_for_votes_webpages = list()

    # get the relevant hrefs for the webpages
    for table_row in table.find_elements_by_tag_name('tr'):
        table_datas = table_row.find_elements_by_tag_name('td')

        if len(table_datas) == 0:
            continue

        current_bill = Bill.initFromTableData(table_datas)

        # for each row, we first want to check if this row represents a bill vote.
        # if it isn't, then just ignore this table row
        if isBill(current_bill):

            # get the processed votes
            curr_href = table_datas[0].find_element_by_tag_name('a').get_attribute('href')
            hrefs_for_votes_webpages.append((curr_href, current_bill))



    # now, get all the data from those pages
    for href in hrefs_for_votes_webpages:
        driver.get(href[0])
        print(getSenatorVotesForOneBill(driver))




        # update the dictionary object












driver = getDriver()
#driver.get("https://www.senate.gov/legislative/LIS/roll_call_lists/roll_call_vote_cfm.cfm?congress=116&session=2&vote=00114")
#driver.get("file:///Users/agaut/PycharmProjects/Politicans/HtmlFilesForTesting/senate_names.html")
driver.get("https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_116_2.htm")
#getSenatorVotesForOneBill(driver)
getVotesForAllBillsForOneYear(driver)

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