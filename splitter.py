# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from collections import defaultdict
from converter import Converter
from cutter import Cutter


class Splitter:

    @staticmethod
    def split_time(elem_list, time_s):
        DATA = defaultdict(list)
        for elem in elem_list:
            time, _ = elem
            if time < time_s:
                DATA[0].append(elem)
            elif time > time_s:
                DATA[1].append(elem)
            else:
                DATA[2].append(elem)
        return DATA

    @staticmethod
    def split_time_list(elem_list, time_list):
        DATA = defaultdict(list)
        time_list = sorted(time_list)
        last = 0
        for i, time_s in enumerate(time_list):
            mem = []
            for elem in elem_list:
                time, _ = elem
                if time < time_s:
                    DATA[i].append(elem)
                else: mem.append(elem)
            elem_list = mem
            last = i + 1
        DATA[last] = elem_list
        return DATA

    @staticmethod
    def split_time_delta(elem_list, hh, mm, ss, ms):
        delta = Converter.timeToX(hh, mm, ss, ms)
        time_list = []
        prev_time, _ = elem_list[0]
        for time, _ in elem_list:
            if time - prev_time > delta:
                time_list.append(time)
            prev_time = time
        return Splitter.split_time_list(elem_list, time_list)

    @staticmethod
    def split_time_delta_seconds(elem_list, max_delta_seconds=30):
        return Splitter.split_time_delta(elem_list, 0, 0, max_delta_seconds, 0)

    @staticmethod
    def split_val(elem_list, value_s):
        time_list = []
        for time, val in elem_list:
            if val == value_s: time_list.append(time)
        return Splitter.split_time_list(elem_list, time_list)

    @staticmethod
    def split_val_list(elem_list, value_list):
        time_list = []
        for value in value_list:
            for time, val in elem_list:
                if val == value: time_list.append(time)
        return Splitter.split_time_list(elem_list, time_list)

    @staticmethod
    def split_val_region(elem_list, region_val_list):
        size = len(elem_list)
        n = len(region_val_list)
        time_list = []
        for j in range(size-n):
            region_found = True
            for i in range(j, j+n):
                _, val = elem_list[i]
                if val != region_val_list[i-j]:
                    region_found = False
                    break
            if region_found:
                time_begin, _ = elem_list[j]
                time_end, _ = elem_list[j+n]
                time_list.append(time_begin)
                time_list.append(time_end)
        time_list = Cutter.remove_duplicates(time_list)
        return Splitter.split_time_list(elem_list, time_list)

    @staticmethod
    def split_elem(elem_list, elem_s):
        j = 0
        for i, elem in enumerate(elem_list):
            if elem == elem_s:
                j = i
                break
        DATA = defaultdict(list)
        if j == 0: DATA[0] = elem_list
        else:
            DATA[0] = elem_list[:j]
            DATA[1] = elem_list[j:]
        return DATA

    @staticmethod
    def split_elem_region(elem_list, region_elem_list):
        size = len(elem_list)
        n = len(region_elem_list)
        if size == 0:
            print("(!) empty source list")
            return defaultdict(list)
        if n == 0:
            print("(!) empty region list")
            return defaultdict(list)
        time_list = []
        for j in range(size-n):
            region_found = True
            for i in range(j, j+n):
                if elem_list[i] != region_elem_list[i-j]:
                    region_found = False
                    break
            if region_found:
                time_begin, _ = elem_list[j]
                time_end, _ = elem_list[j+n]
                time_list.append(time_begin)
                time_list.append(time_end)
        time_list = Cutter.remove_duplicates(time_list)
        return Splitter.split_time_list(elem_list, time_list)

    @staticmethod
    def split_elem_regions_a(elem_list, DATA):
        r_data = defaultdict(list)
        n_data = Splitter.split_elem_region(elem_list, DATA[0])
        r_data[-1] = n_data[0]
        r_data[0] = n_data[1]
        elem_list = n_data[2]
        for i in range(1, len(DATA.keys())-1):
            n_data = Splitter.split_elem_region(elem_list, DATA[i])
            print("##", sep='..', end='')
            r_data[i-1] += n_data[0]
            r_data[i] = n_data[1]
            elem_list = n_data[2]
            if bool(elem_list) is False: break
        print(" ")
        return r_data

    @staticmethod
    def split_elem_regions_a_st(elem_list, DATA, start_time):
        new_data = defaultdict(list)
        i = 0
        for key in DATA.keys():
            # DATA[key] = sorted(DATA[key], key=lambda (t, v): t)
            for time, _ in DATA[key]:
                if time >= start_time:
                    new_data[i] = DATA[key]
                    i += 1
                    break
        return Splitter.split_elem_regions_a(elem_list, new_data)

    @staticmethod
    def split_elem_regions_a_bi(elem_list, DATA, block_index):
        new_data = defaultdict(list)
        i = 0
        for key in DATA.keys():
            if key >= block_index:
                new_data[i] = DATA[key]
                i += 1
        return Splitter.split_elem_regions_a(elem_list, new_data)

    @staticmethod
    def remove_blocks_less_than(DATA, dots_count):
        new_data = defaultdict(list)
        i = 0
        for key in DATA.keys():
            if len(DATA[key]) >= dots_count:
                new_data[i] = DATA[key]
                i += 1
        return new_data

    @staticmethod
    def u_data_to_elem_list(DATA):
        elem_list = []
        for key in DATA.keys():
            elem_list += DATA[key]
        return elem_list

    @staticmethod
    def u_data_to_elem_list_wlb(DATA):
        elem_list = []
        b = len(DATA.keys()) - 1
        for i, key in enumerate(DATA.keys()):
            if i == b: break
            elem_list += DATA[key]
        return elem_list