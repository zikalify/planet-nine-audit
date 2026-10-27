"""Propagation validation.

The fixture rows are REAL published rows from the CaltechDATA v3 reference
population (MD5 a38fa7579b4c9938b3deebecda55a845). The dataset's published
elements carry two decimals, so full-precision published RA/Dec cannot be
reproduced exactly from them; measured scatter (median ~53 arcsec over all
100,000 rows) matches a Monte Carlo of the element rounding. Tolerances
below reflect that documented input-precision limit.
"""

import os
import unittest

import pandas as pd

from p9audit import propagate

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "v3-epoch-check.csv")


class EpochReproductionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(FIXTURE)

    def test_geocentric_radec_at_epoch(self):
        earth = propagate.earth_ecliptic(propagate.EPOCH_V3)
        for _, row in self.df.iterrows():
            ra, dec, r = propagate.geo_radec(row.a, row.e, row.inc, row["varpi"], row.Omega, row.M,
                                             propagate.EPOCH_V3, propagate.EPOCH_V3, earth=(earth[0], earth[1], earth[2]))
            dra = abs((ra - row.ra + 180) % 360 - 180)
            self.assertLess(dra, 0.06, f"row {row['index']}: RA off by {dra} deg")
            self.assertLess(abs(dec - row.dec), 0.06, f"row {row['index']}: Dec off")
            self.assertLess(abs(r - row.R) / row.R, 0.002, f"row {row['index']}: range off")

    def test_earth_position_sanity(self):
        # Earth-Sun distance stays within [0.98, 1.02] AU over a year.
        for jd in range(2458270, 2458270 + 365, 30):
            ex, ey, ez = propagate.earth_ecliptic(float(jd))
            r = (ex ** 2 + ey ** 2 + ez ** 2) ** 0.5
            self.assertTrue(0.98 < r < 1.02)


if __name__ == "__main__":
    unittest.main()
