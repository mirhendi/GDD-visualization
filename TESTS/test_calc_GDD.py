#!/usr/bin/python3
import sys
sys.path.append('..')
sys.path.append('src')

from calc_GDD import calc_GDD

tmin = [10, 11, 12, 12, 12, 16, 20]
tmax = [20, 18, 15, 22, 25, 30, 22]
tbase = [10, 10, 10, 10, 12, 12, 15]

out_put = open('TESTS/test_calc_GDD.act','w')

for i in range(len(tmin)):
    out_put.write('{}\n'.format(calc_GDD(tmin[i], tmax[i], tbase[i])))

out_put.close()
