from solution import contains_duplicate


def test_example_1():
    # [1,2,3,1] → True (1이 중복)
    assert contains_duplicate([1, 2, 3, 1]) is True


def test_example_2():
    # [1,2,3,4] → False (모두 고유)
    assert contains_duplicate([1, 2, 3, 4]) is False


def test_example_3():
    # [1,1,1,3,3,4,3,2,4,2] → True (여러 중복)
    assert contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True


def test_edge_empty():
    # 빈 배열 → False
    assert contains_duplicate([]) is False


def test_edge_single():
    # 원소 1개 → False
    assert contains_duplicate([1]) is False


def test_edge_two_same():
    # 같은 원소 2개 → True
    assert contains_duplicate([1, 1]) is True
