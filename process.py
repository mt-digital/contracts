##
# Download a series of contract announcements for contracts worth more than
# $6.5 million.
#
# Data taken from http://www.defense.gov/contracts/
#
# contracts start at number 391 (October 07, 1994)
#
import os
import warnings

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
            for p in pars:
                # contracting branches are styled (with centering)
                if 'style' in p.attrs.keys() or 'align' in p.attrs.keys():
                    branch = p.get_text().strip().lower()
                    contract_dict[branch] = []
                else:
                    text = p.get_text().strip()
                    if text:
                        contract_dict[branch].append(text)

        # older ones use h3 tags
        except UnboundLocalError as e:
            print e.message
            # we need to iterate over all the elements in the div with cntrcts
            contracts_div = soup.find_all(class_="PressOpsContentBody")[1]

            for el in contracts_div.descendants:

                if el.name == 'h3':
                    branch = el.get_text().strip().lower()
                    if branch:
                        contract_dict[branch] = []

                elif el.name == 'p' and branch:
                    text = el.get_text().strip()
                    if text:
                        contract_dict[branch].append(text)

    date = \
        ','.join(map(lambda s: s.strip(),
                 soup.title.get_text().strip().split(',')[-2:])
                 )

    # key entire dictionary on the date; we'll use it for building time series
    contract_dict = {"date": date, "contracts": contract_dict}

    if save_file:
        with open(save_file, 'w+') as f:
            f.write(dumps(contract_dict))

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
                   and not f.startswith('.')
                   ]

    if output_json_dir[-1] != '/':
        output_json_dir += '/'

    if parallel:
        Parallel(n_jobs=8)(delayed(make_agency_dict)(f) for f in input_files)
    else:
        for f in input_files:
            print f
            basename = os.path.basename(f).split('.')[0] + '.json'
            make_agency_dict(f, output_json_dir + basename)
