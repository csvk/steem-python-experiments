"""
Created on Sun Mar 18 15:05:03 2018

@author: Souvik
"""

from steem.account import Account
from dateutil.parser import parse
import datetime
from dateutil.relativedelta import relativedelta

def vote_history_count(account_name, startdate, enddate):
    """
    - Find the total number of incoming and outgoing votes for any user
    - For the same user, find the number of incoming votes from and outgoing votes to different accounts
    :param account_name: Steemit accountname for which data needs to be fetched
    :param startdate: Reporting period start data YYYY-MM-DD format
    :param enddate: Reporting period end data YYYY-MM-DD format
    :return: Users and incoming, outgoing vote count to and from @account_name
    """

    start, end = datetime.datetime.strptime(startdate, '%Y-%m-%d'), \
                 datetime.datetime.strptime(enddate, '%Y-%m-%d') + relativedelta(hours=23, minutes=59, seconds=59)

    print('Fetching voting history for user @{} for  the period {} to {}...'.format(account_name, start, end))

    posts, authors = {}, {}
    in_votes, out_votes = 0, 0

    for vote in Account(account_name).history_reverse(filter_by="vote"):
        time_voted = parse(vote["timestamp"])
        valid_vote = False
        if time_voted >= start and time_voted <= end:
            permlink = "@{}/{}".format(vote["author"], vote["permlink"])
            if permlink not in posts:
                if vote['weight'] == 0:
                    posts[permlink] = {'votes': 0, 'voters': [vote['voter']]}
                    valid_vote = False
                else:
                    posts[permlink] = {'votes': 1, 'voters': [vote['voter']]}
                    valid_vote = True
            else:
                if vote['voter'] not in posts[permlink]['voters']:
                    if vote['weight'] == 0:
                        posts[permlink]['voters'].append(vote['voter'])
                        valid_vote = False
                    else:
                        posts[permlink]['votes'] = posts[permlink]['votes'] + 1
                        posts[permlink]['voters'].append(vote['voter'])
                        valid_vote = True


            if valid_vote:
                if vote['voter'] == account_name:
                    if vote['author'] not in authors:
                        authors[vote['author']] = {'incoming': 0, 'outgoing': 1}
                    else:
                        authors[vote['author']]['outgoing'] = authors[vote['author']]['outgoing'] + 1
                    out_votes = out_votes + 1
                if vote['author'] == account_name:
                    if vote['voter'] not in authors:
                        authors[vote['voter']] = {'incoming': 1, 'outgoing': 0}
                    else:
                        authors[vote['voter']]['incoming'] = authors[vote['voter']]['incoming'] + 1
                    in_votes = in_votes + 1

        if time_voted < start:
            break

    print('Votes received: {}, votes given: {}'.format(in_votes, out_votes))
    print('Printing vote details...')
    print('Username, Incoming Votes, Outgoing Votes')
    for author in authors:
        print('{}, {}, {}'.format(author, authors[author]['incoming'], authors[author]['outgoing']))

    return authors




vote_history_count(account_name='svkrulze', startdate='2018-03-21', enddate='2018-03-22')