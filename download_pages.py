##
# Download a series of contract announcements for contracts worth more than
# $6.5 million.
#
# Data taken from http://www.defense.gov/contracts/
#
# contracts start at number 391 (October 07, 1994)
#
import os

from urllib2 import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
from json import dumps

def download_announcements(first_id=1842, last_id=5442):
    """
    Download contract announcements for a range of contract IDs from
    http://www.defense.gov/Contracts
    """
    url_root = 'http://www.defense.gov/contracts/contract.aspx?contractid='

    save_dir = "data/html/"
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    # download newest first because that's handier
    ids = [str(valid_num) for valid_num in range(last_id, first_id, -1)]

    # for id_ in ids[-5:]:
    for id_ in ids:

        url = url_root + id_
        page = urlopen(url)
        html = page.read()

        save_file = save_dir + id_ + ".html"
        with open(save_file, 'w') as f:
            f.write(html)

        print "Downloaded ", url


def make_agency_dict(html_file, save_file=None):
    """
    Parse the defense.gov contract html
    """
    soup = BeautifulSoup(open(html_file, 'r'))

    # the first paragraph says "CONTRACTS"
    pars = soup.find_all("p")[1:]

    contract_dict = defaultdict(list)
    for p in pars:
        # contracting branches are styled (with centering)
        if 'style' in p.attrs.keys():
            branch = p.get_text().strip().lower()
            contract_dict[branch] = []
        else:
            text = p.get_text().strip()
            if text:
                contract_dict[branch].append(text)

    if save_file:
        with open(save_file, 'w+') as f:
            f.write(dumps(contract_dict))

    return contract_dict
