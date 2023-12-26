# --------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: (C) 2022 Jayesh Badwaik <j.badwaik@fz-juelich.de>
# --------------------------------------------------------------------------------------------------

import keyso


def test_kvs_set():
    a1 = keyso.kvs({"a": "aval"})
    a2 = keyso.kvs({"a": "bval"})

    b = keyso.kvs_set([a1, a2])
    assert (b.flat_type() == keyso.flat_type(["a"]))

    c = keyso.kvs({"c": "cval"})
    try:
        d = keyso.kvs_set([a1, c])
    except TypeError as e:
        assert str(e) == "kvs_set: kvs types not uniform"

    try:
        d = keyso.kvs_set([a1, a1])
    except TypeError as e:
        assert str(e) == "kvs_set: duplicate kvs in the kvs_set"

    d = keyso.kvs_set([a1, a2])
    e = keyso.kvs({"a": "cval"})
    d.append(e)
    assert d == keyso.kvs_set([a1, a2, e])

    try:
        d.append(a1)
    except TypeError as e:
        assert str(e) == "kvs_set: duplicate kvs in the kvs_set"
