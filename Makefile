all: GDD_Gr01.pdf

SGD.class: src/SGD_linearRegression.java
	javac src/SGD_linearRegression.java 

GDD_Gr01.pdf: doc/GDD_Gr01.tex SGD.class
	pdflatex doc/GDD_Gr01.tex
	rm -f GDD_Gr01.aux GDD_Gr01.log

min_max_plot.py: src/get_new_data.py gdd.py src/place_time_temp_data.sql

min_max_gdd_plot.py: src/get_new_data.py gdd.py src/place_time_temp_data.sql

acc_gdd_plot.py: src/get_new_data.py gdd.py src/place_time_temp_data.sql

gdd.py: src/getfile.py src/stationcsv2sql.py src/check_station_id.py src/station_id_by_province.py src/read_from_sql.py

station_id_by_province.py: src/read_from_sql.py src/stationInventory.sql

check_station_id.py: src/read_from_sql.py src/stationInventory.sql

stationcsv2sql.py: src/read_from_sql.py src/place_time_temp_data.sql

check_database_first.py: src/read_from_sql.py src/place_time_temp_data.sql

get_new_data.py: src/stationcsv2sql.py

getfile.py:

calc_GDD.py:

place_time_temp_data.sql: src/getfile.py

stationInventory.sql: get_stationInventory.py

webpage.html: src/min_max_plot.py src/min_max_gdd_plot.py src/acc_gdd_plot.py


test:
	python3 TESTS/test_GDD.py


clean:
	rm -f GDD_Gr01.log GDD_Gr01.aux GDD_Gr01.pdf GDD_Gr01.out
	rm -f src/SGD.class
	rm -rf __pycache__
	rm -f *.pyc src/*.pyc
	rm -f texput.log
	rm -f *.csv
