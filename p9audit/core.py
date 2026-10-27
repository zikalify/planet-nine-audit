"""Transparent coverage arithmetic on externally generated detection probabilities.

Each row is a model particle, each probability a calibrated survey-level chance
of detecting that particle. No orbit fitting, ephemeris propagation or discovery
claim is performed. Probabilities are conditional on the supplied model.
"""
from __future__ import annotations
import math
from dataclasses import dataclass


def probability(value):
    if isinstance(value, bool):
        raise ValueError("Boolean is not a numeric probability")
    v = float(value)
    if not math.isfinite(v) or not 0 <= v <= 1:
        raise ValueError("Probability must be finite and in [0, 1]")
    return v


@dataclass(frozen=True)
class Particle:
    model: str
    particle: str
    weight: float


@dataclass(frozen=True)
class Search:
    name: str
    group: str
    source: str


class Audit:
    """Dependence within a group is unknown: use probability union bounds.

    Across groups the caller explicitly assumes conditional independence.
    Within a group union detection is bounded by max(p) and min(1, sum(p)).
    Unsearched particles are retained with zero detection probability.
    """
    def __init__(self, particles, searches, detections):
        self.particles = list(particles)
        searches = list(searches)
        self.searches = {s.name: s for s in searches}
        if not self.particles or not self.searches:
            raise ValueError("Particles and searches must be nonempty")
        if len(self.searches) != len(searches):
            raise ValueError("Duplicate search name")
        self.models = sorted({p.model for p in self.particles})
        self.weights = {}
        for p in self.particles:
            key = (p.model, p.particle)
            if not p.model or not p.particle or key in self.weights:
                raise ValueError("Blank or duplicate particle key")
            w = float(p.weight)
            if not math.isfinite(w) or w <= 0:
                raise ValueError("Weights must be finite and positive")
            self.weights[key] = w
        self.totals = {m: sum(w for (model, _), w in self.weights.items() if model == m) for m in self.models}
        if any(not math.isfinite(t) for t in self.totals.values()):
            raise ValueError("Weight totals overflow")
        for s in self.searches.values():
            if not s.name or not s.group or not s.source:
                raise ValueError("Search name, dependence group and provenance required")
        self.detections = {}
        for model, particle, search, p in detections:
            key = (model, particle, search)
            if (model, particle) not in self.weights or search not in self.searches:
                raise ValueError("Unknown particle or search in detections")
            if key in self.detections:
                raise ValueError("Duplicate detection probability")
            self.detections[key] = probability(p)
        # Sparse data are not silently treated as exclusions or nondetections.
        expected = len(self.weights) * len(self.searches)
        if len(self.detections) != expected:
            raise ValueError("Incomplete probability matrix: include explicit zeros for all particles/searches")

    def _groups(self, selected):
        if len(set(selected)) != len(selected):
            raise ValueError("Duplicate selected search")
        groups = {}
        for name in selected:
            if name not in self.searches:
                raise ValueError(f"Unknown search: {name}")
            groups.setdefault(self.searches[name].group, []).append(name)
        return groups

    def coverage(self, selected):
        groups = self._groups(list(selected))
        result = {m: {"lower": 0., "upper": 0.} for m in self.models}
        for (m, particle), w in self.weights.items():
            lower_miss = upper_miss = 1.
            for names in groups.values():
                ps = [self.detections[m, particle, n] for n in names]
                lower_miss *= 1 - min(1., math.fsum(ps))
                upper_miss *= 1 - max(ps)
            result[m]["lower"] += w / self.totals[m] * (1 - upper_miss)
            result[m]["upper"] += w / self.totals[m] * (1 - lower_miss)
        return result

    def marginal(self, selected, candidate):
        """Bounds on gain using joint union bounds, not subtracting two lowers.

        If candidate shares a dependence group, its additional detection within
        that group is bounded by max(0, p-sum(old)) and min(p, 1-max(old)).
        """
        selected = list(selected)
        groups = self._groups(selected)
        if candidate in selected or candidate not in self.searches:
            raise ValueError("Candidate must be a known, unselected search")
        cg = self.searches[candidate].group
        out = {m: {"lower": 0., "upper": 0.} for m in self.models}
        for (m, particle), w in self.weights.items():
            p = self.detections[m, particle, candidate]
            peer = [self.detections[m, particle, s] for s in groups.get(cg, [])]
            lo, hi = max(0., p - sum(peer)), min(p, 1 - max(peer, default=0.))
            for group, names in groups.items():
                if group != cg:
                    ps = [self.detections[m, particle, n] for n in names]
                    lo *= 1 - min(1., sum(ps))
                    hi *= 1 - max(ps)
            out[m]["lower"] += w / self.totals[m] * lo
            out[m]["upper"] += w / self.totals[m] * hi
        return out

    def rank(self, selected):
        rows = []
        for name in sorted(set(self.searches) - set(selected)):
            gain = self.marginal(selected, name)
            rows.append({"search": name, "gain_by_model": gain,
                         "worst_model_lower_gain": min(v["lower"] for v in gain.values())})
        return sorted(rows, key=lambda r: (-r["worst_model_lower_gain"], r["search"]))


def angular_separation(ra1, dec1, ra2, dec2):
    """Stable great-circle angle in degrees, including RA wrap and poles."""
    vals = [float(x) for x in (ra1, dec1, ra2, dec2)]
    if not all(math.isfinite(x) for x in vals) or not (-90 <= vals[1] <= 90 and -90 <= vals[3] <= 90):
        raise ValueError("Finite coordinates and declinations in [-90,90] required")
    a, d, b, e = map(math.radians, vals)
    x = math.cos(e) * math.sin(b-a)
    y = math.cos(d)*math.sin(e) - math.sin(d)*math.cos(e)*math.cos(b-a)
    z = math.sin(d)*math.sin(e) + math.cos(d)*math.cos(e)*math.cos(b-a)
    return math.degrees(math.atan2(math.hypot(x, y), z))
