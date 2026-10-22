import unittest
from page_replacement import fifo, optimal, lru, DEFAULT_REFS


class TestPageReplacement(unittest.TestCase):
    def test_textbook_example_3_frames(self):
        self.assertEqual(fifo(DEFAULT_REFS, 3)[1], 15)
        self.assertEqual(optimal(DEFAULT_REFS, 3)[1], 9)
        self.assertEqual(lru(DEFAULT_REFS, 3)[1], 12)

    def test_belady_anomaly_fifo(self):
        refs = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
        self.assertEqual(fifo(refs, 3)[1], 9)
        self.assertEqual(fifo(refs, 4)[1], 10)  # more frames, more faults

    def test_optimal_never_worse(self):
        for n in range(1, 6):
            o = optimal(DEFAULT_REFS, n)[1]
            self.assertLessEqual(o, fifo(DEFAULT_REFS, n)[1])
            self.assertLessEqual(o, lru(DEFAULT_REFS, n)[1])

    def test_single_frame_all_faults_when_alternating(self):
        self.assertEqual(fifo([1, 2, 1, 2], 1)[1], 4)


if __name__ == "__main__":
    unittest.main()
