import std.datetime;
import std.stdio;
import std.string;

void main()
{
	Clock C;
    writeln("yeah");
    writeln("standard time: ", C.currStdTime,", unix time: ", C.currTime);

    writeln("standard time converted to 'unix time', supposedly in seconds after"
        "1970: ", stdTimeToUnixTime(C.currStdTime) );

    // got to try to convert some shit
    // from docs: "opCall(); UTC is a singleton class. UTC returns its only instance.
    auto dt = SysTime( DateTime(1970, 1, 1), UTC() );
    assert( dt.toUnixTime == 0 );
    writeln( dt.toUnixTime );

    auto dt2 = SysTime( DateTime(1970, getMonth( "JANuary" ), 1), UTC() );
    assert (dt2.toUnixTime == 0);

    // will have to write a large switch to make a mapping for months
}

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
    assert(getMonth("march")     ==  Month.mar);
    assert(getMonth("april")     ==  Month.apr);
    assert(getMonth("may")       ==  Month.may);
    assert(getMonth("june")      ==  Month.jun);
    assert(getMonth("july")      ==  Month.jul);
    assert(getMonth("august")    ==  Month.aug);
    assert(getMonth("september") ==  Month.sep);
    assert(getMonth("october")   ==  Month.oct);
    assert(getMonth("november")  ==  Month.nov);
    assert(getMonth("december")  ==  Month.dec);
}

