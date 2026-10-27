"""Clustering-method validation against every published anchor in
Siraj, Chyba & Tremaine 2026 (ApJ 1003 76), Table 1.

Deviations from the published values come from documented convention
differences (current JPL SBDB element solutions vs the paper's
then-current solutions; heliocentric vs barycentric; first-observation
detection epochs). Tolerances: +-0.15 sigma, +-3 deg; measured deviations
are <=0.05 sigma and <=2 deg. See docs/validation.md.
"""

import os
import unittest

from p9audit import clustering

SAMPLE = os.path.join(os.path.dirname(__file__), "..", "data", "sct26-sample.json")


class AnchorReproductionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = clustering.run_all(SAMPLE)
        cls.comp = clustering.compare_to_anchors(cls.results)

    def test_sample_sizes(self):
        self.assertEqual(self.results["BB21"]["N"], 11)
        self.assertEqual(self.results["SCT25"]["N"], 21)
        self.assertEqual(self.results["SCT26"]["N"], 25)

    def test_all_anchors_within_tolerance(self):
        for method in self.comp:
            for sample in self.comp[method]:
                cell = self.comp[method][sample]
                self.assertTrue(
                    cell["within_tolerance"],
                    f"{method}/{sample}: Z={cell['Z']:.2f} (pub {cell['Z_published']}), "
                    f"dir={cell['direction_deg']:.1f} (pub {cell['direction_published']})",
                )

    def test_significance_ordering(self):
        # Published behaviour: SCT25 sample strengthened, SCT26 weakened below BB21.
        z = {s: self.results[s]["cl3d"]["Z"] for s in ("BB21", "SCT25", "SCT26")}
        self.assertGreater(z["SCT25"], z["BB21"])
        self.assertLess(z["SCT26"], z["BB21"])


if __name__ == "__main__":
    unittest.main()


class ProfileIntervalTest(unittest.TestCase):
    def test_sct26_3d_interval_matches_published(self):
        sample = clustering.load_sample(SAMPLE)
        subsets = clustering.sample_subsets(sample)
        r = clustering.profile3d_direction(subsets["SCT26"])
        # Published SCT26 Table 1: 151 deg (+34/-59); tolerances match anchor policy
        self.assertAlmostEqual(r["ml_lon"], 151.0, delta=3.0)
        self.assertAlmostEqual(r["plus_deg"], 34.0, delta=3.0)
        self.assertAlmostEqual(r["minus_deg"], 59.0, delta=3.0)
