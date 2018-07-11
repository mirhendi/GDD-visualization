#!/usr/bin/python3

#Code for testing
import os
import time
import sys
sys.path.append('..')
sys.path.append('src')

print('Checking python3 modules.')

Error_modules = os.popen("python3 TESTS/dependencies.py").read()

if Error_modules == 'All modules are OK!\n':
    print(Error_modules)

print('Checking tests for calc_GDD')

os.popen('python3 TESTS/test_calc_GDD.py')
time.sleep(1)
Error_calc_GDD = os.popen("diff TESTS/test_calc_GDD.exp TESTS/test_calc_GDD.act; echo $?").read()

if Error_calc_GDD == "0\n":
    print('Tests were successful.')
    os.popen('rm -f TESTS/test_calc_GDD.act')
else:
    sys.exit('Test for calc_GDD failed:\n', Error_calc_GDD)

print('Checking test for read_from_sql')

os.popen('python3 gdd.py province -r newfoundland')
time.sleep(1)
Error_read_from_sql = os.popen("diff *NEWFOUNDLAND.txt TESTS/NEWFOUNDLAND.txt; echo $?").read()

if Error_read_from_sql == "0\n":
    print('Test was successful.')
    os.popen('rm -f *NEWFOUNDLAND.txt')
else:
    sys.exit('Test for read_from_sql failed:\n', Error_read_from_sql)

print('Checking test for gdd.py station')

check = os.popen('python3 gdd.py station -g toronto').read()
File = open('toronto_station.act', 'w')
time.sleep(1)
for line in check.split('\n'):
	File.write('{}\n'.format(line))
File.close()

Error_gdd_station = os.popen("diff toronto_station.act TESTS/toronto_station.exp; echo $?").read()

if Error_gdd_station == "0\n":
    print('Test was successful.')
    os.popen('rm -f toronto_station.act')
else:
    sys.exit('Test for gdd.py station failed:\n', Error_gdd_station)

print('All tests are OK!')
