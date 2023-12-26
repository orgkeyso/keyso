# --------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: (C) 2022 Jayesh Badwaik <j.badwaik@fz-juelich.de>
# --------------------------------------------------------------------------------------------------

import keyso


def test_kvs():
    a = keyso.kvs({"a": "aval"})
    b = keyso.kvs({"b": "bval"})

    c = a * b

    assert a.flat_type().underlying_value() == ["a"]
    assert b.flat_type().underlying_value() == ["b"]
    assert c == keyso.kvs({"a": "aval", "b": "bval"})
    assert c.flat_type().underlying_value() == ["a", "b"]

    d = keyso.kvs({"a": "aval"})

    try:
        e = a * d
    except TypeError as e:
        assert str(e) == "kvs: kvs types not compatible"

    try:
        e = d * a
    except TypeError as e:
        assert str(e) == "kvs: kvs types not compatible"

    try:
        f = {"a": {"b": "c"}}
        g = keyso.kvs(f)
    except TypeError as e:
        assert str(e) == "kvs: kvs is not flattened"
