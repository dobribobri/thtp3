# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function


class Cutter:
    def __init__(self, lower_threshold=None, upper_threshold=None, start_time=None, stop_time=None):
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        self.start_time = start_time
        self.stop_time = stop_time
        if not(lower_threshold or upper_threshold or start_time or stop_time):
            print("Nothing to cut!")

    @staticmethod
    def cut_all_above_lower_thr(elem_list_2d, lower_threshold):
        new_list = []
        if lower_threshold is not None:
            for time, val in elem_list_2d:
                if val >= lower_threshold:
                    new_list.append((time, val))
            elem_list_2d = new_list
        return elem_list_2d

    @staticmethod
    def cut_all_below_upper_thr(elem_list_2d, upper_threshold):
        new_list = []
        if upper_threshold is not None:
            for time, val in elem_list_2d:
                if val <= upper_threshold:
                    new_list.append((time, val))
            elem_list_2d = new_list
        return elem_list_2d

    def cut_val(self, elem_list_2d):
        elem_list_2d = self.cut_all_above_lower_thr(elem_list_2d, self.lower_threshold)
        return self.cut_all_below_upper_thr(elem_list_2d, self.upper_threshold)

    @staticmethod
    def cut_all_after_start_time(elem_list_2d, start_time):
        new_list = []
        if start_time is not None:
            for time, val in elem_list_2d:
                if time >= start_time:
                    new_list.append((time, val))
            elem_list_2d = new_list
        return elem_list_2d

    @staticmethod
    def cut_all_before_stop_time(elem_list_2d, stop_time):
        new_list = []
        if stop_time is not None:
            for time, val in elem_list_2d:
                if time <= stop_time:
                    new_list.append((time, val))
            elem_list_2d = new_list
        return elem_list_2d

    def cut_time(self, elem_list_2d):
        elem_list_2d = self.cut_all_after_start_time(elem_list_2d, self.start_time)
        return self.cut_all_before_stop_time(elem_list_2d, self.stop_time)

    def cut(self, elem_list_2d):
        elem_list_2d = self.cut_time(elem_list_2d)
        return self.cut_val(elem_list_2d)

    def cut_d_time(self, DATA, key=None):
        if key is not None:
            DATA[key] = self.cut_time(DATA[key])
        else:
            for key in DATA.keys():
                DATA[key] = self.cut_time(DATA[key])
        return DATA

    def cut_d_val(self, DATA, key=None):
        if key is not None:
            DATA[key] = self.cut_val(DATA[key])
        else:
            for key in DATA.keys():
                DATA[key] = self.cut_val(DATA[key])
        return DATA

    def cut_d(self, DATA, key=None):
        return self.cut_d_val(self.cut_d_time(DATA, key), key)

    @staticmethod
    def remove_duplicates(elem_list):
        new_elem_list = []
        if len(elem_list) == 0: return elem_list
        prev = elem_list[0]
        new_elem_list.append(prev)
        for elem in elem_list:
            if elem == prev: continue
            new_elem_list.append(elem)
            prev = elem
        return new_elem_list