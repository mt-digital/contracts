/**
 * Some functions and corresponding script to make post #1's data.
 */
import std.algorithm : canFind, filter, findSplitAfter, findSplitBefore, map,
    reduce;
import std.array : array, join;
import std.math : fmax;
import std.range : chain, iota;
import std.container : SList;
import std.conv : to;
import std.csv : csvReader;
import std.datetime : SysTime, DateTime, UTC;
import std.exception : enforce;
import std.stdio : File, writeln;
import std.string : format;


string[] topFive  = 
    [ "Lockheed Martin",
      "McDonnell Douglas",
      "Boeing",
      "Mullen",
      "ADI Technology" // <- only one huge contract for them! woah!
    ];

immutable uint nDays = 365 * 3;

void main()
{
    const string fullCsv = "data/proc/contracts_2001_2003.csv";
    const string writeCsv = "vis/data/p1_ts_data.csv";
    writeTopFiveTs(fullCsv, writeCsv);

    //string x = "heyyo aw";
    //string y = x.findSplitAfter("gg")[0];
    //assert (y == "");
    //writeln(y == ""); <- yes this works
}

void writeTopFiveTs(const string fullCsv, const string writeCsv)
{
    // load csv rows
    auto rawCsvLines = File(fullCsv, "r").byLine();
    enforce (rawCsvLines.front == "Date,Amount,Contractor");

    // strip header
    rawCsvLines.popFront();
    // process csv rows
    auto procCsvRows = rawCsvLines.map!(l => csvReader!ProcCsvRow(l).front);
   
    // generate full range of possible contract dates--all days jan 1, 2001 to dec 31, 2003 
    auto firstSysDay = SysTime(DateTime(2001,1,1), UTC());

    double oneDayDiff = 
        SysTime(DateTime(2001,1,2), UTC()).toUnixTime - firstSysDay.toUnixTime;

    double[] days = 
        iota(nDays).map!(i => firstSysDay.toUnixTime + i*oneDayDiff).array;

    // establish SLists keyed on top5 contractor name
    SList!(ProcCsvRow)[string] normalizedNameRows;
    foreach (c; topFive)
        normalizedNameRows[c] = *(new SList!ProcCsvRow);

    string s;
    foreach(row; procCsvRows)
    {
        foreach (c; topFive)
        {  /*
            * see if the company name can be found in the first part
            * if so, take the first entry in the split, which is the name.
            *  given in `topFive` 
            */

            s = row.Contractor
                   .findSplitAfter( c )[0];
            if (s != "")
            {
            	// insert a new ProcCsvRow with standardized name
                normalizedNameRows[ c ]
                    .insert( ProcCsvRow(row.Date, row.Amount, c) );
            }
        }
    }
    
    // make "contractor series" with every day in the three years; zeros where no contracts made
    ContractorSeries[] series;// = new ContractorSeries[5];
    foreach (i, c; topFive)
       series ~= contractorSeries(days, normalizedNameRows[c].array); 

    // for each contractor series, make the amounts the cumulative sum
    double total;
    foreach (ref c; series)
    {
        total = 0.0;
        writeln(c.name);
        foreach (d; c.amounts.keys.sort)
        {
        	total += c.amounts[d];
            c.amounts[d] = total;
        }
    }

    // write cumulate sum to file
    auto writeFile = File(writeCsv, "w");
    writeFile.writeln("day," ~ topFive.join(","));
    string rowDataStr;
    //double[] rowData = new double[5];
    foreach (i, day; days)
    {
        rowDataStr = series.map!(a => a.amounts[day])
                           .map!(val => format("%.8f",val))
                           .array
                           .join(",");

        writeFile.writeln(format("%.8f,",day) ~ rowDataStr);
    }
}

ContractorSeries contractorSeries(
                    double[] fullTimeRange, // in unixEpoch
                    ProcCsvRow[] normalizedNameRows)
{
    // initialize full array
    double[double] amountByDay;
    foreach (d; fullTimeRange)
        amountByDay[d] = 0.0;
    
    string name = normalizedNameRows[0].Contractor;
    foreach (row; normalizedNameRows)
    {
    	enforce( row.Contractor == name, format(
    	    "The CSV rows' contractor names are not all identical: found topFive: %s, from data: %s",
    	    name, row.Contractor) 
    	);

    	writeln( amountByDay.keys.reduce!"fmax(a,b)" );
    	if( auto ptr = row.Date in amountByDay )
    		*ptr = row.Amount;
    	
    	else
    	   throw new Exception(row.Date.to!string ~ " day not found in fullTimeRange");
    }
        
    return ContractorSeries(name, amountByDay.keys, amountByDay);
}

/**
 * Holds a contractor series.
 */
struct ContractorSeries 
{
	private struct Entry { double val = 0.0; alias val this; }

    string name;
    double[] index;
    double[double] amounts;
}


struct ProcCsvRow
{
    double Date, Amount;
    string Contractor;
}

