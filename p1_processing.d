/**
 * Some functions and corresponding script to make post #1's data.
 */
import std.algorithm : canFind, filter, findSplitAfter, findSplitBefore, map;
import std.array : array;
import std.conv : to;
import std.csv : csvReader;
import std.exception : enforce;
import std.stdio : File, writeln;


const string[] topFive  = 
[ "Lockheed Martin",
  "McDonnell Douglas",
  "Boeing",
  "Mullen",
  "ADI Technology" // <- only one huge contract for them! woah!
];

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
    // strip header, find top-five entries
    rawCsvLines.popFront();

    auto procCsvRows = rawCsvLines.map!(l => csvReader!ProcCsvRow(l).front);

    // write top-five entries to file
    auto writeFile = File(writeCsv, "w");
    string s;
    foreach(row; procCsvRows)
    {
        foreach( c; topFive )
        {
        	// see if the company name can be found in the first part
            s = row.Contractor
                   .findSplitAfter( c )[0];
            // if so, take the first entry in the split, which is the name
            //  given in `topFive` 
            if (s != "")
                writeFile.writeln(row.Date.to!string ~ "," 
                                ~ row.Amount.to!string ~ "," 
                                ~ s.findSplitBefore( c )[1]);
        }
    }
}

struct ProcCsvRow
{
    double Date, Amount;
    string Contractor;
}
