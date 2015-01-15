"""
Module: process.py

For various processing tasks of contract data.

Definitions:
    Activity- A DoD technical term that I'm currently (mis)using to refer to
              subgroups within the DoD, e.g. Army, Navy, Defense Information
              Systems Agency, Missile Defense Agency, etc.
"""
##
# Download a series of contract announcements for contracts worth more than
# $6.5 million.
#
# Data taken from http://www.defense.gov/contracts/
#
# contracts start at number 391 (October 07, 1994)
#
import os
import re

from urllib2 import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
from json import dumps
from joblib import Parallel, delayed


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
        with open(save_file, 'w') as file_:
            file_.write(html)

        print "Downloaded ", url


def make_agency_dict(html_file, save_file=None):
    """
    Parse the defense.gov contract html
    """
    soup = BeautifulSoup(open(html_file, 'r'))

    # the first paragraph says "CONTRACTS"
    pars = soup.find_all("p")[1:]

    contract_dict = defaultdict(list)

    # Not all IDs in the range actually have data. For example,
    # http://www.defense.gov/Contracts/Contract.aspx?ContractID=5052
    # redirects to defense.gov homepage
    if "defense.gov" not in soup.title.get_text():
        # one case
        # (http://www.defense.gov/Contracts/Contract.aspx?ContractID=5067)
        # found to not have a first agency, only "contracts" so use
        # "contracts" as default
        branch = "contracts"
        # newer contracts use bolded, centered paragraphs for agency
        try:
            for par in pars:
                # contracting branches are styled (with centering)
                if 'style' in par.attrs.keys() or 'align' in par.attrs.keys():
                    branch = par.get_text().strip().lower()
                    contract_dict[branch] = []
                else:
                    text = par.get_text().strip()
                    if text:
                        contract_dict[branch].append(text)

        # older ones use h3 tags
        except UnboundLocalError as err:
            print err.message
            # we need to iterate over all the elements in the div with cntrcts
            contracts_div = soup.find_all(class_="PressOpsContentBody")[1]

            for elem in contracts_div.descendants:

                if elem.name == 'h3':
                    branch = elem.get_text().strip().lower()
                    if branch:
                        contract_dict[branch] = []

                elif elem.name == 'p' and branch:
                    text = elem.get_text().strip()
                    if text:
                        contract_dict[branch].append(text)

    date = \
        ','.join([s.strip() for s in
                  soup.title.get_text().strip().split(',')[-2:]])

    # key entire dictionary on the date; we'll use it for building time series
    contract_dict = {"date": date, "contracts": contract_dict}

    if save_file:
        with open(save_file, 'w+') as file_:
            file_.write(dumps(contract_dict))

    return contract_dict


def make_agency_dicts(html_dir="data/html", output_json_dir="data/json",
                      parallel=True):
    """
    Use ``make_agency_dict`` to clean the html and save the json format to
    file, keyed by defense agency.
    """
    if not os.path.isdir(output_json_dir):
        os.makedirs(output_json_dir)

    if html_dir[-1] != '/':
        html_dir += '/'

    input_files = [html_dir + f for f in os.listdir(html_dir)
                   if os.path.isfile(html_dir + f)
                   and not f.startswith('.')]

    if output_json_dir[-1] != '/':
        output_json_dir += '/'

    if parallel:
        Parallel(n_jobs=8)(delayed(make_agency_dict)(f) for f in input_files)
    else:
        for file_ in input_files:
            print file_
            basename = os.path.basename(file_).split('.')[0] + '.json'
            make_agency_dict(file_, output_json_dir + basename)


def unzip_fgdc():
    """
    Assume a directory structure as can be understood from the simple code
    below.
    """
    to_dir = "data/fgdc/"
    from_dir = "data/archive/"

    for file_ in os.listdir(from_dir):
        full_to_dir = to_dir + re.findall("20[01][0-9]", file_)[0]
        if not os.path.isdir(full_to_dir):
            os.makedirs(full_to_dir)
        os.popen("unzip " + from_dir + "'" + file_ + "'" +
                 " -d " + full_to_dir)


def count_by_activity(contract_json):
    """
    Given a full JSON contracts dictionary, return a new dictionary of counts
    by activity.
    """
    by_activity = contract_json['contracts']
    activities = by_activity.keys()

    return dict(zip(activities, [len(by_activity[a]) for a in activities]))

def make_contract_row(contract_json):
    """

    """

    return ContractRow()


class ContractRow(object):
    """
    Contract row contains the following fields, a container for the information
    gleaned from a contract announcement.
    """
    def __init__(self, arg):
        self.arg = arg

    def as_string(self):
        """
        Return a comma-separated string of the extracted fields of the contract
        from the contract announcement.
        """
        pass
