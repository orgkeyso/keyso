# --------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: (C) 2022 Jayesh Badwaik <j.badwaik@fz-juelich.de>
# --------------------------------------------------------------------------------------------------

import typing
import json
import functools
import itertools


class flat_type:
    def __init__(self, array: typing.List[str]):
        if not isinstance(array, list):
            raise TypeError("type: argument not a list")
        for value in array:
            if not isinstance(value, str):
                raise TypeError("type: element not a string")
        self._value = array

    def compatible(self, other: typing.Self):
        if not isinstance(other, flat_type):
            raise TypeError("type: argument not a type")
        return set(self._value).isdisjoint(set(other._value))

    def __eq__(self, other):
        if len(self._value) == 0 or len(other._value) == 0:
            return True
        return self._value == other._value

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return str(self._value)

    def underlying_value(self):
        return self._value


def is_kvs(dictionary: dict):
    if not isinstance(dictionary, dict):
        raise TypeError("kvs: argument not a dictionary")
    for key, value in dictionary.items():
        if not isinstance(key, str):
            raise TypeError("kvs: keys not a string")
        if not isinstance(value, str):
            raise TypeError("kvs: kvs is not flattened")


class kvs:
    def __init__(self, dictionary: dict):
        is_kvs(dictionary)
        self._kvs = dictionary

    def flat_type(self):
        return flat_type(list(self._kvs))

    def __getitem__(self, key):
        return self._kvs[key]

    def __setitem__(self, key, value):
        self._kvs[key] = value

    def __mul__(self, other: typing.Self):
        result = {}
        if not isinstance(other, kvs):
            raise TypeError("kvs: argument not a kvs")
        if not self.flat_type().compatible(other.flat_type()):
            raise TypeError("kvs: kvs types not compatible")
        for key, value in self._kvs.items():
            result[key] = value
        for key, value in other._kvs.items():
            result[key] = value

        return kvs(result)

    def __rmul__(self, value: typing.Self):
        self.__mul__(value)

    def __eq__(self, other):
        return self._kvs == other._kvs

    def __hash__(self):
        return hash(json.dumps(self._kvs))


def is_kvs_set(array: typing.List[kvs]):
    if len(array) != len(set(array)):
        raise TypeError("kvs_set: duplicate kvs in the kvs_set")

    if not isinstance(array, list):
        raise TypeError("kvs_set: argument not a list")

    if not isinstance(array[0], kvs):
        raise TypeError("kvs_set: argument not a kvs")

    initial_type = array[0].flat_type()
    for value in array:
        if value.flat_type() != initial_type:
            raise TypeError("kvs_set: kvs types not uniform")


class kvs_set:
    def __init__(self, array: typing.List[kvs]):
        is_kvs_set(array)
        self._kvs_set = array

    def flat_type(self):
        return self._kvs_set[0].flat_type()

    def isdisjoint(self, other: typing.Self):
        return self._kvs_set.isdisjoint(other._kvs_set)

    def __mul__(self, other: typing.Self):
        return itertools.product(self._kvs_set, other._kvs_set)

    def __getitem__(self, key: int):
        if not isinstance(key, int):
            raise TypeError("kvs_set: key not an integer")
        return self._kvs[key]

    def __eq__(self, other: typing.Self):
        if not isinstance(other, kvs_set):
            raise TypeError("kvs_set: argument not a kvs_set")
        return self._kvs_set == other._kvs_set

    def append(self, value: kvs):
        if not isinstance(value, kvs):
            raise TypeError("kvs_set: value is not a kvs")

        if value.flat_type() != self.flat_type():
            raise TypeError("kvs_set: value type not uniform")

        self._kvs_set.append(value)


# class product:
#    def __init__(self, dictionary: dict):
#        self._product = dictionary
#
#    def type(self):
#        value_type = []
#        for key, value in self._product.items():
#            if key == "_comment":
#                continue
#            elif key == "_product" and isinstance(value, dict):
#                product_type = product(value).type()
#                for type_name in product_type:
#                    value_type.append(type_name)
#            elif key == "_union" and isinstance(value, list):
#                value_type.append(union(value).type())
#            elif isinstance(value, list):
#                value_type.append(key)
#            else:
#                raise TypeError("product: unsupported value type at key " +
#                                key + " with value " + str(value))
#
#        return value_type
##
# def flat_value(self):
# result = []
# for key, value in self._product.items():
# if key == "_comment":
# continue
# elif key == "_product":
# product_value = product(value).flat_value()
# for kvs in result:
# for key, array_value in product_value.items():
# for value in array_value:
# kvs = kvs * {key: value}
# elif isinstance(key, str) and isinstance(value, list):
# result.append(key)
# else:
# raise TypeError("product: unsupported value type")
##
##
#
#
# class union:
#    def __init__(self, value: list):
#        if not isinstance(value, list):
#            raise TypeError("union: value is not a list")
#
#        if not isinstance(value[0], dict):
#            raise TypeError("union: value is not a list of dictionaries")
#
#        base_type = product(value[0]).type()
#        for element in value:
#            if element.compute_type() != base_type:
#                raise TypeError("union: value type not homogenous")
#        self._union = value
#        self._type = base_type
#
#    def type(self):
#        return self._type
#
#
# def parse(input: json):
#    if isinstance(input, dict):
#        return product(input)
#    elif isinstance(input, list):
#        return union(input)
