import unittest

from benchmark.operations.time_mem_approximations import Time_Mem_Approx_Instructions


class TestSum(unittest.TestCase):
    def test_single_perfect_overlap(self):
        hist_1 = ([5], [0, 1])
        hist_2 = ([10], [0, 1])

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)

        self.assertEqual(selectivity, 1)

    def test_single_half_overlap(self):
        hist_1 = ([5], [0, 1])
        hist_2 = ([10], [0, 2])

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)

        self.assertEqual(selectivity, 0.5)

    def test_two_perfect_overlaps(self):
        hist_1 = ([5, 5], [0, 1, 2])
        hist_2 = ([5, 5], [0, 1, 2])

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)

        self.assertEqual(selectivity, 0.5)

    def test_two_weighted_overlaps(self):
        hist_1 = ([5, 10], [0, 1, 5])
        hist_2 = ([5, 10], [0, 1, 5])

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)

        self.assertEqual(selectivity, (5 * 5 + 10 * 10) / (15 * 15))

    def test_two_weighted_shifted_overlaps(self):
        hist_1 = ([5, 10], [0, 1, 2])
        hist_2 = ([5, 10], [0, 1, 3])

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)

        self.assertEqual(selectivity, (5 * 5 + 10 * 5) / (15 * 15))

    def test_two_weighted_shifted_overlaps_inverted(self):
        hist_1 = ([5, 10], [0, 1, 3])
        hist_2 = ([5, 10], [0, 1, 2])

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)

        self.assertEqual(selectivity, (5 * 5 + 10 * 5) / (15 * 15))

    def test_no_overlaps(self):
        hist_1 = ([5], [0, 1])
        hist_2 = ([5], [1, 2])

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)

        self.assertEqual(selectivity, 0)

    def test_shifted_overlap(self):
        hist_1 = ([3, 3, 3, 3], [0, 1, 2, 3, 4])
        hist_2 = ([5, 5], [3, 4, 5])

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)

        self.assertEqual(selectivity, 15 / 120)

    def test_almost_no_overlaps(self):
        o = 0.001

        hist_1 = ([5], [0 + o, 1 + o])
        hist_2 = ([5], [1, 2])

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)

        self.assertAlmostEqual(selectivity, (5 * o * 5 * o) / (5 * 5))

    def test_cover(self):
        hist_1 = ([12], [1, 4])
        hist_2 = ([6], [2, 3])

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)

        self.assertEqual(selectivity, (4 * 6) / (12 * 6))

    def test_cover_inv(self):
        hist_2 = ([12], [1, 4])
        hist_1 = ([6], [2, 3])

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)

        self.assertEqual(selectivity, (4 * 6) / (12 * 6))

    def test_run_off(self):
        hist_2 = ([1, 1, 1, 1, 1], [1, 2, 3, 4, 5, 6])
        hist_1 = ([1, 1], [0, 1, 2])

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)
        self.assertEqual(selectivity, 1 / (2 * 5))

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_2, hist_1)
        self.assertEqual(selectivity, 1 / (2 * 5))

    def test_partial(self):
        hist_2 = ([2, 2, 2, 2, 2], [1, 2, 3, 4, 5, 6])
        hist_1 = ([5], [1.5, 2])

        overlap = 5 * 1

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)
        self.assertEqual(selectivity, overlap / (sum(hist_1[0]) * sum(hist_2[0])))

    def test_partial_2(self):
        hist_2 = ([2, 2, 2, 2, 2], [1, 2, 3, 4, 5, 6])
        hist_1 = ([5], [1.5, 2.5])

        selectivity = ((5.0 / 2 / 5) * (2.0 / 2 / 10)) + ((5.0 / 2 / 5) * (2.0 / 2 / 10))

        selectivity = Time_Mem_Approx_Instructions().sel_join_hist(hist_1, hist_2)
        self.assertEqual(selectivity, selectivity)


if __name__ == "__main__":
    unittest.main()
