##
# Found a way to make a timeseries of contract values/counts awarded by the DoD
# per day since 1994, as long as the contract was valued at $6.5 mil.
#
# Data taken from http://www.defense.gov/contracts/
#


# contracts start at number 391 (October 07, 1994)
from __future__ import unicode_literals
from urllib2 import urlopen
from bs4 import BeautifulSoup
#from pandas import DataFrame

# found this on so:
# http://stackoverflow.com/questions/1342000/how-to-make-the-python-interpreter-correctly-handle-non-ascii-characters-in-stri
def removeNonAscii(s): return "".join( i for i in s if ord(i)<128 )

# eventually we'll loop over each one, but for now, 
# just take dollar vals, date, and description
url_root = 'http://www.defense.gov/contracts/contract.aspx?contractid='
# 5171: November 22, 2013
#valid_suffixes = [ str( valid_num ) for valid_num in range(391, 5172) ]
# this one starts Jan 2011
#valid_suffixes = [ str( valid_num ) for valid_num in range(4441, 5172) ]
# Jan 2001 - Dec 2003
#valid_suffixes = [ str( valid_num ) for valid_num in range(1926, 2668) ]
# Jan 1998 - Dec 2000
#valid_suffixes = [ str( valid_num ) for valid_num in range(1188, 1925) ]
# Jan 2004 - Jan 2008
#valid_suffixes = [ str( valid_num ) for valid_num in range(4575, 5210) ]
# Oct 1994 - Dec 1997
valid_suffixes = [ str( valid_num ) for valid_num in range(391, 1187) ]

write_file = open( 'data/dod_contracts_ts_Oct04-1994_1997.csv', 'w' )
# initialize columns of csv file
write_file.write('Date,Dollar Amount,Full Description\n')

for suffix in valid_suffixes:
#for suffix in valid_suffixes[-10:-8]:
    # open the next day's contracts page
    page = urlopen( url_root + suffix )
    html = page.read()
    soup = BeautifulSoup( html )
    # extract <p> html elements
    paragraphs = [ p.getText().replace(u'\xa0',u'') for p in soup.find_all('p') ]
    # get the date out of the title
    date = ' '.join( soup.title
                         .getText()
                         .split(' ')[-3:] #.encode( 'utf-8' )
                     ).replace(',', '').replace('\n','').replace('\r','')
    print "grabbing data for " + date                         

    # iterate over p elements, find the ones with dollar values--these are
    #  also the ones with actual records, not other filler
    for p in paragraphs:

	    dollar_split = p.split('$') 

	    # take only the dollar amount, remove commas, and convert to float
	    if len( dollar_split ) > 1:
	    	
	    	dollar_amt = dollar_split[1].split(' ')[0] \
	    	                            .replace(',', '') \
	    	                            .replace('\n', '') \
	    	                            .replace('\r', '')

            # append to file
	    	write_file.write( u','.join( [
                date.encode('utf-8'), str(dollar_amt), 
                    removeNonAscii(p).replace('\n','').replace('\r','')
	    	    ]) + '\n'
	    	)

write_file.close()
	    	    
