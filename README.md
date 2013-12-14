contracts
=========

Tools and data for exploring US Federal Government contracts

Log
---

12/13/12
********
Revisiting after a little break. Have some functions to get the 
month and date epoch, which will be useful for web viz. My plan for 
processing the 'raw' csv is to have a 'process CSV' function, which will
process the CSV by-line, but with successive improvements, like scraping out
the location, company name, contract code, and important bits of the 
description like 'missile defense', 'fire control', or 'small arms training.'
For processed data, scrap the full description. Keep it always in the raw files.
The raw CSV come from scraping defense.gov contract announcements.

For now, extract the epoch date and the company name. The functionality for
transforming a date like 'December 12, 2013' to an Unix-time epoch is written
with unittests. To extract the company name, split and take the first element
on `','`. 

But following agile/lean principles means getting one thing working first.
So, I also need to write the functionality to transform the raw file to just
epoch-coded date and amount. This is the first product. Second product is a 
processed file with the amount, the company name, and the date.

Then, I want to make a plot with Vincent that makes a stacked timeseries plot,
a stacked timeseries difference plot, and also an 'acceleration' plot. Compare
the acceleration of dollars spent to something mechanical and military, 
like the acceleration of an F-15, a Humvee, or something else.

Also it'd be interesting to do some relative variance analysis, or other stats
with R.

