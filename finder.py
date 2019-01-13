# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
import sys


class Finder:

    @staticmethod
    def find_elem_index_first(elem_list, elem_f):
        # Находит индекс эл-та = elem_f в 2d-списке при проходе слева направо
        # Если эл-т не найдет, возвращает -1
        for i, elem in enumerate(elem_list):
            if elem == elem_f:
                return i
        return -1

    @staticmethod
    def find_elem_index_last(elem_list, elem_f):
        # Находит индекс эл-та = elem_f в 2d-списке при проходе справа налево
        # Если эл-т не найдет, возвращает -1
        for i in range(len(elem_list) - 1, -1, -1):
            if elem_list[i] == elem_f:
                return i
        return -1

    @staticmethod
    def find_elem_index(elem_list, elem_d):
        # Эквивалент find_elem_index_first(elem_list, elem_f)
        return Finder.find_elem_index_first(elem_list, elem_d)

    @staticmethod
    def find_elem_t(elem_list, time_el):
        for time, val in elem_list:
            if time == time_el:
                elem = (time, val)
                return elem
        return (-1, -1)

    @staticmethod
    def find_elem_index_t(elem_list, time_el):
        i = 0
        for time, val in elem_list:
            if time == time_el:
                return i
            i += 1
        return -1

    @staticmethod
    def find_nearest_elem_t_(elem_list, time_el):
        # Найти первый эл-т в 2d-списке, для которого time >= time_el
        # Если такой эл-т не найден, возвращается последний
        for time, val in elem_list:
            if time >= time_el:
                elem = (time, val)
                return elem
        return elem_list[len(elem_list) - 1]

    @staticmethod
    def find_nearest_elem_index_t_(elem_list, time):
        # Найти индекс первого эл-та в 2d-списке, для которого time >= time_el
        # Если такой эл-т не найден, возвращается индекс последнего эл-та
        i = 0
        for time_el, _ in elem_list:
            if time_el >= time:
                return i
            i += 1
        return len(elem_list) - 1

    @staticmethod
    def find_nearest_elem_index_t(elem_list, time):
        # Найти в 2d-списке индекс первого ближайшего к заданному времени эл-та
        min_delta = sys.maxint
        index = 0
        i = 0
        for t, _ in elem_list:
            delta = abs(t - time)
            if delta < min_delta:
                min_delta = delta
                index = i
            i += 1
        return index

    @staticmethod
    def find_nearest_elem_t(elem_list, time):
        # Найти в 2d-списке первый ближайший к заданному времени эл-т
        index = Finder.find_nearest_elem_index_t(elem_list, time)
        return elem_list[index]

    @staticmethod
    def find_nearest_elem_v(elem_list, value_el):
        # Найти в 2d-списке первый ближайший по значению эл-т
        index = Finder.find_nearest_elem_index_v(elem_list, value_el)
        return elem_list[index]

    @staticmethod
    def find_nearest_elem_index_v(elem_list, value):
        # Найти в 2d-списке индекс первого ближайшего по значению эл-та
        min_delta = sys.maxint
        index = 0
        i = 0
        for _, val in elem_list:
            delta = abs(val - value)
            if delta < min_delta:
                min_delta = delta
                index = i
            i += 1
        return index

    @staticmethod
    def find_nearest_block_index_t(DATA, time):
        # Найти в DATA индекс блока, содержащего ближайший
        # к заданному времени эл-т
        mem = []
        for key in DATA.keys():
            # DATA[key] = sorted(DATA[key], key=lambda (t, v): t)
            k1, k2 = 0, 0
            for t, _ in DATA[key]:
                if t == time: return key
                elif t < time: k1 += 1
                else: k2 += 1
            l = len(DATA[key])
            if k1 == l:
                t, _ = DATA[key][l - 1]
                mem.append((key, abs(t - time)))
                continue
            if k2 == l:
                t, _ = DATA[key][0]
                mem.append((key, abs(t - time)))
                continue
            return key
        min_delta = sys.maxint
        r_key = 0
        for key, delta in mem:
            if delta < min_delta:
                min_delta = delta
                r_key = key
        return r_key