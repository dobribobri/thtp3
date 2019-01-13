# -*- coding: utf-8 -*-
from __future__ import print_function
from matplotlib import pyplot as plt
from parser import Parser
from converter import Converter
from splitter import Splitter
from cutter import Cutter
from finder import Finder

FILENAME = "P22M_2018_04_15__09-57-57.dat_tb.txt"
FILENAME = FILENAME[:25] + "_V_FP_" + FILENAME[25:]
t_file = open("psql-lab-dat/file-dir/" + FILENAME, "r")
t_file.readline()
elem_list = []
for line in t_file:
    l_data = Parser.parse_line(line)
    if len(l_data) < 10: continue
    hh, mm, ss = l_data[1].split(':')
    ms = l_data[2]
    timestamp = Converter.timeToX(hh, mm, ss, ms)
    elem_list.append((timestamp, float(l_data[6]), float(l_data[9])))
    elem_list.append((timestamp, float(l_data[8]), float(l_data[9])))
t_file.close()

shift = 170

TIME, TEMP, THETA = [], [], []
for time, temp, theta in elem_list:
    if theta == 0: continue
    TIME.append(time)
    THETA.append(theta)
    TEMP.append(temp+shift)
plt.plot(TIME, THETA)
plt.plot(TIME, TEMP)
plt.show()
plt.close()

'''
theta_list = [114, 115, 120, 130, 145, 160]
remove_interval = Converter.timeToX(0,0,10,0)
ANSWER = []
for i, th in enumerate(theta_list):
    TIME, TEMP, THETA = [], [], []
    data_list = []
    for time, temp, theta in elem_list:
        if th == theta:
            data_list.append((time, temp))
    DATA = Splitter.remove_blocks_less_than(Splitter.split_time_delta_seconds(data_list, 30), 10)
    for key in DATA.keys():
        time_begin, _ = DATA[key][0]
        time_end, _ = DATA[key][len(DATA[key]) - 1]
        DATA[key] = \
            Cutter(start_time=time_begin + remove_interval, stop_time=time_end - remove_interval).cut(DATA[key])
    data_list = Splitter.u_data_to_elem_list(DATA)
    for time, temp in data_list:
        ANSWER.append(time)
        TIME.append(time)
        TEMP.append(temp)
    i += 1
    plt.figure(i)
    plt.title(str(th))
    # plt.plot(TIME, THETA)
    plt.plot(TIME, TEMP, "b+")
plt.show()
'''

theta_list = [114, 115, 120, 130, 145, 160]
for i, th in enumerate(theta_list):
    TIME, TEMP, THETA = [], [], []
    data_list = []
    for time, temp, theta in elem_list:
        if th == theta:
            data_list.append((time, temp))
    for time, temp in data_list:
        TIME.append(time)
        TEMP.append(temp)
    i += 1
    plt.figure(i)
    plt.title(str(th))
    plt.plot(TIME, TEMP, "b+")
plt.show()

'''
t0_file = open("psql-lab-dat/file-dir/" + FILENAME, "r")
FILENAME = FILENAME.replace("_V_1_", "_V_FP_")
w_file = open("psql-lab-dat/file-dir/" + FILENAME, "w")
str0 = t0_file.readline()
w_file.write(str0)
i = 0
for line in t0_file:
    if i % 1000 == 0: print("#", sep='..', end='')
    l_data = Parser.parse_line(line)
    hh, mm, ss = l_data[1].split(':')
    ms = l_data[2]
    timestamp = Converter.timeToX(hh, mm, ss, ms)
    found = False
    for time in ANSWER:
        if time == timestamp:
            w_line = l_data[0] + "\t" + l_data[1] + " " + l_data[2] + "\t" +\
                    l_data[3] + "\t" + l_data[4] + "\t" + l_data[5] + "\t" +\
                    l_data[6] + "\t" + l_data[7] + "\t" + l_data[8] + "\t" +\
                    l_data[9]
            w_file.write(w_line + "\n")
            found = True
            break
    i += 1
    if found: continue
    w_line = l_data[0] + "\t" + l_data[1] + " "  + l_data[2] + "\t" + \
             l_data[3] + "\t" + l_data[4] + "\t" + l_data[5] + "\t" + \
             l_data[6] + "\t" + l_data[7] + "\t" + l_data[8] + "\t" + \
             "0"
    w_file.write(w_line + "\n")
t0_file.close()
w_file.close()
'''