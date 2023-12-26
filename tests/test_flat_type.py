# --------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: (C) 2022 Jayesh Badwaik <j.badwaik@fz-juelich.de>
# --------------------------------------------------------------------------------------------------


import keyso

def test_construction():
    a = keyso.flat_type(["a", "b", "c"])
    b = keyso.flat_type(["a", "b", "c"])
    c = keyso.flat_type(["a", "b", "d"])
    d = keyso.flat_type(["d", "e", "f"])

    assert str(a) == "['a', 'b', 'c']"
    assert a == b
    assert a != c
    assert a != d
    assert a.compatible(d)



