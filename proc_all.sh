#!/bin/bash
##
# Script to process the csv files build from daily > $6.5M on dod site
# found in the 'clean' folder
#

make process_clean_csv -B

./process_clean_csv \
-inputFile=data/clean/clean_contracts_1998_2000.csv \
-outputFile=data/proc/contracts_1998_2000.csv

./process_clean_csv \
-inputFile=data/clean/clean_contracts_2004_2008.csv \
-outputFile=data/proc/contracts_2004_2008.csv

./process_clean_csv \
-inputFile=data/clean/clean_contracts_2009_2014.csv \
-outputFile=data/proc/contracts_2009_2014.csv

./process_clean_csv \
-inputFile=data/clean/clean_contracts_2001_2003.csv \
-outputFile=data/proc/contracts_2001_2003.csv




