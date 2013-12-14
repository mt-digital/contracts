
export UT = -unittest

test_clean_raw_csv: cleanRawDodCSV.d
	dmd ${UT} $^ -of$@ && ./test_clean_raw_csv && rm test_clean_raw_csv.o	

clean_raw_csv: cleanRawDodCSV.d
	dmd $^ -of$@ # then call ./clean_raw_csv with args --{out,in}File=f.csv

test_process_clean_csv: processCleanDodCSV.d
	dmd ${UT} $^ -of$@ && ./test_process_raw_csv && rm test_process_clean_csv.o	

process_clean_csv: processCleanDodCSV.d
	dmd $^ -of$@ # then call ./process_clean_csv with args --{out,in}File=f.csv

clean:
	rm *.o clean_raw_csv process_clean_csv
