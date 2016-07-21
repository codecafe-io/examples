# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import unittest
import infection_statistics

class InfectionStatisticsTest(unittest.TestCase):

        def test_infections_statistics(self):
                itemCount = infection_statistics.queryByCity(cityName="Reno")
                self.assertEqual(178, itemCount)

if __name__ == '__main__':
        unittest.main()

