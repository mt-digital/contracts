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
import fuzzywuzzy as fuzz
import os
import re

from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime
from json import dumps
from urllib2 import urlopen


def download_announcements(first_id=1842, last_id=5442, save_dir="data/html/"):
    """
    Download contract announcements for a range of contract IDs from
    http://www.defense.gov/Contracts.
    """
    url_root = 'http://www.defense.gov/contracts/contract.aspx?contractid='

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


def make_agency_dicts(html_dir="data/html", output_json_dir="data/json"):
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

    expr = re.compile("20[01][0-9]")

    for file_ in os.listdir(from_dir):
        full_to_dir = to_dir + re.findall(expr, file_)[0]
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


def make_contract_jsons(contract_blob, date, division):
    """
    parse a day's worth of contracts in JSON format to be a list of
    dictionaries where every single contract announcement (blob) is parsed and
    made into a row of a dataframe.

    Returns: Array (most will be len 1) of parsed-out json strings.
    """
    # parse in to sentences. first sentence is the company announcement.
    # split on ';' because sometimes have mult companies sep'd by ';'.
    # if multiple, create multiple contract_json. handle multiple

    # dollar amounts

    # percentage per company

    #

    contract_jsons = []

    return [js for js in contract_jsons]

##########################################
# Helper functions for make_contract_row
#
#     Parameters: blob_lines
#        A single announcement, a child of division, grandchild of date,
#        assumed split into lines by sentence with nltk sent_tokenize.
##########################################


def _extract_company_roots(blob):
    """
    Find all companies and return a list of lists of their 'roots'.
    For example, Lockheed Martin Aerospace, LTD would result in
    ["Lockheed ", "Martin ", "Aerospace"]. Other things like lowering
    all upper case and stripping will be done when we build the
    normalized list of companies, so if we had "Lockheed Martin Fire
    and Missile", we would match that to "Lockheed Martin Aerospace"
    giving both a normalized name "Lockheed Martin"
    """
    assert isinstance(blob, basestring), \
        "Error, must pass a string blob, not %s" % str(type(blob))

    semicol_split = blob.split(';')
    to_comma = [el.split(',')[0] for el in semicol_split]

    get_company_roots = lambda x: re.findall("[A-Z][a-zA-Z.]*\s*", x.strip())

    company_roots = map(get_company_roots, to_comma)

    return company_roots


#: Regex to extract, e.g., $343,444,400 from a string
find_dollars = \
    lambda x: re.findall("\$[0-9]{1,3},[0-9]{1,3},[0-9]{1,3}[,0-9]*", x)

#: Convert find_dollars-found string to integer
doll_to_int = lambda x: int(x.replace('$', '').replace(',', ''))


def _extract_amount(blob_lines):
    "Extract dollar amounts from blob lines. If multiple, sum them"
    assert type(blob_lines) is list

    string_dollars = reduce(list.__add__, map(find_dollars, blob_lines))

    total_dollars = reduce(int.__add__,
                           [doll_to_int(sd) for sd in string_dollars])

    return total_dollars


class ContractRow(object):
    """
    Contract row contains the following fields, a container for the information
    gleaned from a contract announcement.
    """
    def __init__(self, row_dict):

        assert row_dict.keys() == ["date", "division", "company",
                                   "related_ids", "amount", "pct_shared"]

        assert type(row_dict["date"]) is datetime
        self.date = row_dict["date"]

        self.division = row_dict["division"]
        self.company = row_dict["company"]
        self.related_ids = row_dict["related_ids"]
        self.amount = row_dict["amount"]
        self.pct_shared = row_dict["pct_shared"]


def normalize_company_list(company_list):
    """
    transform the list of companies to be normalized, meaning companies with
    important words in common be mapped to a common name when they match to
    a high enough degree
    """
    strip_names = [n.strip().lower() for n in company_list]

    cur_name = company_list[0].strip().lower()

    match_idxs = []
    for i, matching_name in enumerate(strip_names):

        for j, next_name in enumerate(strip_names):

            if fuzz.ratio(cur_name, next_name.strip().lower()) > 75:
                match_idxs.append(j)

        # can improve the make_normalized_name as necessary
        company_list[match_idxs] =\
            make_normalized_name(company_list[match_idxs])

    return company_list


def make_normalized_name(matches):
    """
    Create a single normalized name for all the names for which a
    match has been found.
    """
    # TODO make a smarter version of this?
    if len(matches[0]) == 1:
        return matches[0]
    else:
        return ' '.join(matches[0], matches[1])


def make_csv_contracts():
    """
    make a csv string representing the fully-processed JSONs.
    """
    pass
