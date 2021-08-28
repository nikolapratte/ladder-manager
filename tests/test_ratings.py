from ..ladder_manager.rating_calculators import calculate_match, base_rating_change, \
    calculate_ratings, inequality_change_rate

def test_calculate_match_p1_favored_win():
    delta = base_rating_change - (100//inequality_change_rate)
    assert calculate_match(1300, 1200, True) == (1300 + delta, 1200 - delta)

def test_calculate_match_p1_favored_loss():
    delta = base_rating_change + (100//inequality_change_rate)
    assert calculate_match(1300, 1200, False) == (1300 - delta, 1200 + delta)

def test_calculate_match_p2_favored_win():
    assert calculate_match(1200, 1300, False) == (1180, 1320)

def test_calculate_match_p2_favored_loss():
    assert calculate_match(1200, 1300, True) == (1230, 1270)

def test_calculate_match_p1_ultra_favored_win():
    assert calculate_match(2000, 1200, True) == (2001, 1199)

def test_calculate_match_p2_ultra_favored_win():
    assert calculate_match(1300, 2000, False) == (1299, 2001)

def test_calculate_match_p1_ultra_favored_loss():
    assert calculate_match(2000, 1200, False) == (1950, 1250)

def test_calculate_match_p2_ultra_favored_loss():
    assert calculate_match(1300, 2000, True) == (1350, 1950)

def test_calculate_match_p1_favored_win_rounding():
    assert calculate_match(1851, 1714, True) == (1870, 1695)

def test_calculate_match_p2_favored_win_rounding():
    assert calculate_match(1684, 1914, False) == (1670, 1928)

def test_calculate_match_equal_ratings_p1_win():
    assert calculate_match(1200, 1200, True) == (1225, 1175)

def test_calculate_match_equal_ratings_p1_loss():
    assert calculate_match(1300, 1300, False) == (1275, 1325)

def test_calculate_ratings_simple():
    assert calculate_ratings(1200, 1200, "1") == (1200 + base_rating_change, 1200 - base_rating_change)

def test_calculate_ratings_domination_p1():
    delta1 = base_rating_change - (100//inequality_change_rate)
    delta2 = base_rating_change - ((100 + delta1 * 2)//inequality_change_rate)
    delta3 = base_rating_change - ((100 + delta1 * 2 + delta2 * 2)//inequality_change_rate)
    delta = delta1 + delta2 + delta3
    assert calculate_ratings(1300, 1200, "111") == (1300 + delta, 1200 - delta)

def test_calculate_ratings_domination_p2():
    delta = 20 + 18 + 17
    assert calculate_ratings(1200, 1300, "000") == (1200 - delta, 1300 + delta)