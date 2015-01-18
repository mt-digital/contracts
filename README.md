contracts
=========

Tools and data for exploring US Federal Government contracts

what it is
==========

I want to show how much money comes to defense companies every day and highlight
the perpetual "winners" in this system. I'll do this by parsing the [daily
contract announcements](http://www.defense.gov/contracts/) from the 
Department of Defense website. This isn't about whether or not we should be
carrying out particular missions or even if we spend too much on defense. 
Instead, this is to show the scale at which individual corporations profit from
what is in many cases public-funded high-tech research. 

More and more, it seems
that the public should be reimbursed for its high-risk investment just like
the angel investors of Silicon Valley.

how to use it
=============

In this short example I show the current working functionality. So far we 
provide functionality for downloading raw html pages for each day of contract
announcements and a function for extracting the announcements from the html
into a JSON string, one for each day. The resulting JSON looks like this:

```
{
    "date": "December 19, 2014",
    "contracts": 
    {
        "navy": [
    "General Dynamics National Steel and
     Shipbuilding Co., San Diego, California, is being awarded a $498,116,529
    modification to a previously awarded fixed-price-incentive, firm-target contract
    (N00024-09-C-2229) for the procurement of the detail, design and construction of the fourth Mobile Landing Platform Afloat Forward Staging Base. Work will be performed in: San Diego,
    California (70 percent); Pittsburgh, Pennsylvania (7 percent); Chesapeake, Virginia (7
    percent); Beloit, Wisconsin (6 percent); Iron Mountain, Michigan (2 percent); and various
    locations in the United States (0.8 percent); work is expected to be completed by March 2018.
    Fiscal 2014 shipbuilding and conversion (Navy) contract funds in the amount of
    $498,116,529 will be obligated at time of award and will not expire at the end of the current
    fiscal year. The Naval Sea Systems Command, Washington, District of Columbia, is the
    contracting activity.",
    
    "The Boeing Co., Seattle, Washington, is being awarded a not-to-exceed ..."
```

download contract announcement html
-----------------------------------

You can go to an individual day's contract
announcements, for example, by visiting a URL like this: 
`http://www.defense.gov/Contracts/Contract.aspx?ContractID=391`. That happens
to be the very first one available, October 7, 1994. The latest one as of
this writing is January 16, 2015,
`http://www.defense.gov/Contracts/Contract.aspx?ContractID=5460`. The function


```python
# download about ten years of daily raw contract HTML announcements
download_announcements(first_id=1842, last_id=5442):
# do the same, but instead of default data/html dir, use custom
download_announcements(first_id=1842, last_id=5442, save_dir="raw_html"):
```

convert raw html to JSON
------------------------

```python
# create processed JSON saved to json from raw_html 
# (defaults are data/html to data/json)
make_agency_dicts
```

Finally at its simplest you could just run

```python
download_announcements()
make_agency_dicts()
```

and you will download roughly ten years' worth of daily contract data, first
the whole HTML page for each day to a day-coded `.html` file in `data/html` and
then process those pages to be in the nicely-formatted JSON above, again one
`.json` for every day, in `data/json`.

unittests
=========

Run em with [nosetests](https://nose.readthedocs.org/en/latest/):

```bash
nosetests -v
```

I much prefer the verbose mode. Why even write tests if you don't look at what
they're doing?
