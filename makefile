export UT = -unittest

test_process_clean_csv: processCleanDodCSV.d
	dmd ${UT} $^ -of$@ && ./$@ && rm test_process_clean_csv.o	

process_clean_csv: processCleanDodCSV.d
	dmd -ofbin/$@ $^ -version=main # then call ./process_clean_csv with args --{out,in}putFile=f.csv

clean:
	rm *.o
