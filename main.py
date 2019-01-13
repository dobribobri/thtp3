# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
import re
import os
import glob
import sys
from switch import Switch
from collections import defaultdict
from matplotlib import pyplot as plt
from converter import Converter
from parser import Parser
from cutter import Cutter
from finder import Finder
from splitter import Splitter


def printer(out_list):
    for elem in out_list:
        print(elem)


def printer_d(DATA, key):
    print(key)
    printer(DATA[key])


def plot2d(elem_list):
    x = []
    y = []
    for elem in elem_list:
        a, b = elem
        x.append(a)
        y.append(b)
    plt.plot(x, y, 'r+')


def plot_d_key(DATA, key):
    plot2d(DATA[key])
    plt.show()
    plt.close()


def plot_d(DATA):
    for key in DATA.keys():
        plot2d(DATA[key])
    plt.show()
    plt.close()


def r_len(DATA):
    l = 0
    for key in DATA.keys():
        if len(DATA[key]) != 0: l += 1
    return l


def e_len(DATA):
    return r_len(DATA) - 2


def invert(elem_list, a, b):
    for i in range(len(elem_list)):
        elem_list[i] = b - elem_list[i] + a
    return elem_list


ANSWER = []
FILENAME = "P22M_2018_04_15__09-57-57.dat_tb.txt"

print("\nTH-DATA")
lDATA = Parser("th", "psql-lab-dat/lab-dat/").parse()
cht_l_list = Cutter(upper_threshold=60).cut(lDATA["az"])
cht_lDATA = Splitter.split_time_delta_seconds(cht_l_list)
del cht_l_list
print("Участков по ЧТ: ", len(cht_lDATA.keys()))

print("\nF-DATA")
fDATA = Parser("tb2", "psql-lab-dat/file-dir/" + FILENAME).parse()
'''
freq_range = [11400, 9800, 9900, 10000, 10100, 10200, 10300, 10400, 10500, 10600, 10700, 10800,
              10900, 11000, 11100, 11200, 11300, 11500, 11600, 11700, 11800, 11900,
              12000, 12100, 12200, 12300, 12400, 12500, 12600, 12700, 12800]
'''
freq_range = [11400]
freq_range += range(9800, 11400, 100)
freq_range += range(11500, 12900, 100)
print(" ")
print(freq_range)
print(" ")
k, delta, DELTA = 0, 0, 0

for FREQ in freq_range:
    print("\n\nFREQ is ", FREQ)
    # plot_d_key(fDATA, 18800)
    cht_f_list = Cutter(lower_threshold=150).cut(fDATA[FREQ])
    cht_fDATA = Splitter.remove_blocks_less_than(Splitter.split_time_delta_seconds(cht_f_list), 3)
    del cht_f_list
    print("Участков по ЧТ: ", len(cht_fDATA.keys()))
    f_DATA = Splitter.split_elem_regions_a(fDATA[FREQ], cht_fDATA)
    print(len(cht_fDATA.keys()), " --> ", len(f_DATA.keys()))
    #plot_d(f_DATA)
    t0, _ = f_DATA[0][0]

    f_index = Finder.find_nearest_block_index_t(cht_lDATA, t0)
    print("f_index: :", f_index)
    tf, _ = cht_lDATA[f_index][0]
    #lDATA["az"] = Cutter.cut_all_after_start_time(lDATA["az"], tf)
    # lDATA["v1"] = Cutter.cut_all_after_start_time(lDATA["v1"], tf)
    l_DATA = Splitter.split_elem_regions_a_bi(lDATA["az"], cht_lDATA, f_index)
    print("DATA length: ", len(l_DATA.keys()))
    # plot_d(l_DATA)

    print(" ")
    t1, _ = l_DATA[0][0]
    if delta == 0:
        delta = t1 - t0

    l = e_len(f_DATA)
    T0, _ = f_DATA[l][0]
    T1, _ = l_DATA[l][0]
    if DELTA == 0:
        DELTA = T1 - T0
    del l_DATA

    if k == 0:
        k = DELTA - delta

    print("t0 = ", t0, "   t1 = ", t1)
    print("delta = ", delta)
    print("T0 = ", T0, "   T1 = ", T1)
    print("DELTA = ", DELTA)
    print("k = ", k)
    print(" ")

    temp_list = Splitter.u_data_to_elem_list_wlb(f_DATA)
    # az_list = Splitter.u_data_to_elem_list_wlb(l_DATA)
    theta_list = Cutter(start_time = t1 - DELTA, stop_time = T1 + DELTA).cut(lDATA["v1"])

    ANSWER_ = []
    i = 0
    for Ty0, temp in temp_list:
        if i % 100 == 0: print("####", sep='..', end='')
        Ty1 = Ty0 + delta + k*(Ty0 - t0)/(T0 - t0)
        time, theta = Finder.find_nearest_elem_t(theta_list, Ty1)
        # time_, theta_ = Finder.find_nearest_elem_t_(theta_list, Ty1)
        #TIME = abs(Ty1 + Ty0)/2
        TIME = Ty0
        ANSWER.append((TIME, theta, temp))
        ANSWER_.append((TIME, theta, temp))
        i += 1

    '''
    print(" ")
    l = len(ANSWER_)
    for i in range(l):
        print(ANSWER_[i])
        # print(ANSWER[i], "  -- VS --  ", ANSWER_[i])
    '''

    shift = 170
    TIME, THETA, TEMP = [], [], []
    for time, theta, temp in ANSWER_:
        TIME.append(time)
        THETA.append(theta)
        TEMP.append(temp+shift)
    #plt.plot(TIME, THETA)
    #plt.plot(TIME, TEMP)
    #plt.show()
    #plt.close()

    '''
    print("\n\n")
    A = []
    for i in range( 1, len(ANSWER) - 1 ):
        _, prev_theta, _ = ANSWER[i - 1]
        _, next_theta, _ = ANSWER[i + 1]
        time, theta, temp = ANSWER[i]
        if theta != prev_theta and theta != next_theta: continue
        if theta == prev_theta and theta != next_theta: continue
        if theta != prev_theta and theta == next_theta: continue
        A.append(ANSWER[i])
    
    l = len(A)
    print(len(ANSWER), "   ------>   ", l, '\n')
    for i in range(l):
        print(A[i])
    
    shift = 170
    TIME, THETA, TEMP = [], [], []
    for time, theta, temp in A:
        TIME.append(time)
        THETA.append(theta)
        TEMP.append(temp+shift)
    plt.plot(TIME, THETA)
    plt.plot(TIME, TEMP)
    plt.show()
    plt.close()
    '''

    # y1 = b - y0 + a
    THETA = invert(THETA, 114, 160)

    # for i in range(len(THETA)):
    #    if THETA[i] == 160: THETA[i] = 300

    CORR = []
    for j in range(31):
        corr = 0
        nTHETA = THETA
        for i in range(j):
            for kk in range(len(nTHETA) - 1):
                nTHETA[kk] = nTHETA[kk + 1]
            nTHETA[len(nTHETA) - 1] = 0
        kk = 0
        for i in range(len(TEMP)):
            if nTHETA[i] != 0:
                corr += TEMP[i] * nTHETA[i] / 360 / 150
                kk += 1
        corr /= kk
        CORR.append(corr)

    for j in range(31):
        corr = 0
        nTHETA = THETA
        for i in range(j):
            nTHETA.insert(0, 0)
            del nTHETA[len(nTHETA) - 1]
        kk = 0
        for i in range(len(TEMP)):
            if nTHETA[i] != 0:
                corr += TEMP[i] * nTHETA[i] / 360 / 150
                kk += 1
        corr /= kk
        CORR.append(corr)

    #plt.plot(CORR)
    #plt.show()
    #plt.close()


print(" ")
print(" Writing... ")
t0_file = open("psql-lab-dat/file-dir/" + FILENAME, "r")
str0 = t0_file.readline()
FILENAME = FILENAME[:25] + "_V_" + FILENAME[25:]
t1_file = open("psql-lab-dat/file-dir/" + FILENAME, "w")
t1_file.write(str0[:len(str0)-2] + "\tV\n")
elem_list = []
for line in t0_file:
    l_data = Parser.parse_line(line)
    hh, mm, ss = l_data[1].split(':')
    ms = l_data[2]
    timestamp = Converter.timeToX(hh, mm, ss, ms)
    elem_list.append((timestamp, line))
t0_file.close()
l = len(elem_list)
for i in range(l):
    time, line = elem_list[i]
    line = line[:len(line) - 2]
    elem_list[i] = (time, line)

i = 0
for time, theta, _ in ANSWER:
    if i % 1000 == 0: print("#", sep='..', end='')
    index = Finder.find_nearest_elem_index_t(elem_list, time)
    time_cur, line = elem_list[index]
    line += '\t' + str(theta)
    elem_list[index] = (time_cur, line)
    i += 1

for _, line in elem_list:
    t1_file.write(line + '\n')
t1_file.close()





