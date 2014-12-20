##
# Download a series of contract announcements for contracts worth more than
# $6.5 million.
#
# Data taken from http://www.defense.gov/contracts/
#
# contracts start at number 391 (October 07, 1994)
#
from __future__ import unicode_literals
from urllib2 import urlopen

url_root = 'http://www.defense.gov/contracts/contract.aspx?contractid='

# as of Dec 19 (TODO: Generalize to look up: go to www.defense.gov/contracts)
current_id = 5442
# TODO: accept this as a command line parameter
days_back = 3650  # (ten years)
oldest_id = current_id - days_back

ids = [str(valid_num) for valid_num in range(5442, 1842)]

# for id_ in ids[-5:]:
for id_ in ids:

    url = url_root + id_
    page = urlopen(url)
    html = page.read()

    save_file = "data/raw_html" + id_ + ".html"
    with open(save_file, 'w') as f:
        f.write(html)

    print("Downloaded ", url)
