##
# Simple script to convert amounts to numeric and aggregate the totals per 
# company
#
# Usage:
# Rscript R/aggCompanies.R data/proc/dateAmtCompany.csv data/proc/company_totals.csv

args <- commandArgs(TRUE)

readCsvPath <- args[1]
writeCsvPath <- args[2]


df <- read.csv(readCsvPath, strip.white=TRUE,
        col.names=c('date','amount','company'))

# R dataframe columns are 'factors' .. or something..
df$amount <- as.numeric( as.character(df$amount) )
df <- na.omit(df)

dfAgg <- aggregate(amount ~ company, df, sum)

dfAggSort <- dfAgg[with(dfAgg, order(-amount)), ]

write.csv(dfAggSort, writeCsvPath, row.names=FALSE)

