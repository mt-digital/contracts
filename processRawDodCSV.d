/**
 * Functions for processing the raw csv files gotten through scraping of the
 * DoD site http://www.defense.gov/contracts/, built using python script 
 * dod_contracts_ts.py
 */
module processRawDodCSV;


import std.conv : to;
import std.datetime : Month, DateTime, SysTime, UTC;
import std.math : approxEqual;
import std.string : split, toLower;

/**
 * Convert the 'word dates' found in the 'Date' column of the raw csv to 
 * unix time epochs for use with Rickshaw/d3
 */

void main()
{

}

double wordDateToEpoch(string wordDate)
{
    string[] spl = wordDate.split(" ");
    return SysTime( 
        DateTime(spl[2].to!uint, spl[0].getMonth, spl[1].to!uint)
        ).toUnixTime;
}
unittest {
	double nov10_2013 = SysTime( DateTime(2013, 11, 10), UTC() ).toUnixTime;
    assert ( approxEqual(wordDateToEpoch("november 10 2013"), nov10_2013));

    double apr01_1970 = SysTime( DateTime(1970, 4,  1), UTC() ).toUnixTime;
    assert ( approxEqual(wordDateToEpoch("April 01 1970"), apr01_1970));
}

/**
 * Convert a 'word month', e.g. February, to its representative Month enum
 * member from std.datetime.
 */
ubyte getMonth( string monthWord )
{
    switch (monthWord.toLower) {
    	default:
    	    throw new Exception("An invalid month was found: " ~ monthWord);

        case "january": return Month.jan;
        case "february": return Month.feb;
        case "march": return Month.mar;
        case "april": return Month.apr;
        case "may": return Month.may;
        case "june": return Month.jun;
        case "july": return Month.jul;
        case "august": return Month.aug;
        case "september": return Month.sep;
        case "october": return Month.oct;
        case "november": return Month.nov;
        case "december": return Month.dec;
    }
}

unittest {
	import std.exception;

    assertThrown( getMonth("hooziewhatsit") );
    assertThrown( getMonth("janury")        );

    assert( getMonth("JaNuAry")  ==  Month.jan);
    assert( getMonth("February") ==  Month.feb);
    assert(getMonth("March")     ==  Month.mar);
    assert(getMonth("April")     ==  Month.apr);
    assert(getMonth("May")       ==  Month.may);
    assert(getMonth("june")      ==  Month.jun);
    assert(getMonth("july")      ==  Month.jul);
    assert(getMonth("august")    ==  Month.aug);
    assert(getMonth("September") ==  Month.sep);
    assert(getMonth("October")   ==  Month.oct);
    assert(getMonth("November")  ==  Month.nov);
    assert(getMonth("December")  ==  Month.dec);
}

struct RawContractAnnouncement
{
    string date;
    double dollarAmt;
    string fullDescription;
}
