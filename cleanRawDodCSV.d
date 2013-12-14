/**
 * Functions for processing the raw csv files gotten through scraping of the
 * DoD site http://www.defense.gov/contracts/, built using python script 
 * dod_contracts_ts.py
 */
module cleanRawDodCSV;


import std.algorithm : equal, filter, map, reduce;
import std.array : array, join;
import std.container : SList;
import std.conv : to;
import std.csv : csvReader;
import std.datetime : Month, DateTime, SysTime, UTC;
import std.exception : enforce;
import std.getopt;
import std.math : approxEqual;
import std.range : chunks, drop, take;
import std.string : format, split, strip, toLower;
import std.stdio; 

/**
 * Convert the 'word dates' found in the 'Date' column of the raw csv to 
 * unix time epochs for use with Rickshaw/d3
 */
void main(string[] args)
{
    string inputFile, outputFile;
    bool cleanFirst;
    getopt( args,
        "inputFile|i", &inputFile, 
        "outputFile|o", &outputFile
    );

    cleanRawFile(inputFile, outputFile); 

    //if (cleanFirst)  ## Put these in separate modules with sep mains ##
    //{
        //cleanRawFile(inputFile, outputFile); 
        ////processCleanedFile(outputFile); TODO once the line split is fixed, process it here
    //}
    //else
        ////processCleanedFile(inputFile, outputFile);
}

void cleanRawFile(string inputPath, string outputPath)
{
	auto inFile = File( inputPath, "r" );
	auto csvLines = inFile.byLine();
	// pop the front, check that it's correct.
    enforce (csvLines.front == "Date,Dollar Amount,Full Description",
        "Column titles must be 'Date','Dollar Amount','Full Description'"
    );
	auto outFile = File( outputPath, "w" );
	outFile.writeln( csvLines.front );
    // ready csvLines for iteration over non-col title rows
    csvLines.popFront();


	auto noBlankLines = csvLines.filter!`a != ""`;

    string row1, row2, fullRow;
    // some lines are actually split between two. if a line ends with a comma
    //  join the current line and the next line, and write to output
    foreach (row; noBlankLines)
    {
        row1 = row.idup;	
        if (row1[$-1] == ',')
        {
        	noBlankLines.popFront();
            row2 = noBlankLines.front.idup;
            fullRow = row1 ~ row2;
        }
        else 
        	fullRow = row1;

        outFile.writeln(fullRow);
    }

    outFile.close();
}

