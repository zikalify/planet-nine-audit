import itertools
import math
import unittest
from p9audit.core import Audit, Particle, Search, angular_separation, probability


def make(ps=(.6,.5), same=True, weights=(1,)):
    particles = [Particle('m',str(i),w) for i,w in enumerate(weights)]
    searches = [Search(str(j),'g' if same else str(j),'toy') for j in range(len(ps))]
    return Audit(particles,searches,[('m',str(i),str(j),p) for i in range(len(weights)) for j,p in enumerate(ps)])


class Core(unittest.TestCase):
    def test_unknown_dependence_bounds(self):
        self.assertEqual(make().coverage(['0','1'])['m'], {'lower':.6,'upper':1.})
    def test_independent(self):
        self.assertAlmostEqual(make(same=False).coverage(['0','1'])['m']['lower'], .8)
    def test_empty(self):
        self.assertEqual(make().coverage([])['m'], {'lower':0.,'upper':0.})
    def test_zero_one(self):
        self.assertEqual(make((0,1)).coverage(['0','1'])['m'], {'lower':1.,'upper':1.})
    def test_duplicate_selected(self):
        with self.assertRaises(ValueError): make().coverage(['0','0'])
    def test_unknown_selected(self):
        with self.assertRaises(ValueError): make().coverage(['x'])
    def test_existing_candidate(self):
        with self.assertRaises(ValueError): make().marginal(['0'],'0')
    def test_bad_probability(self):
        for p in (-.1,1.1,float('nan'),float('inf'),True):
            with self.assertRaises(ValueError): probability(p)
    def test_bad_weights(self):
        for w in (0,-1,float('nan'),float('inf')):
            with self.assertRaises(ValueError): make(weights=(w,))
    def test_incomplete_matrix(self):
        with self.assertRaises(ValueError): Audit([Particle('m','a',1)],[Search('s','g','toy')],[])
    def test_duplicate_detection(self):
        with self.assertRaises(ValueError): Audit([Particle('m','a',1)],[Search('s','g','toy')],[('m','a','s',0)]*2)
    def test_duplicate_particle(self):
        with self.assertRaises(ValueError): Audit([Particle('m','a',1)]*2,[Search('s','g','toy')],[])
    def test_provenance_required(self):
        with self.assertRaises(ValueError): Audit([Particle('m','a',1)],[Search('s','g','')],[])
    def test_weight_scale_invariance(self):
        self.assertEqual(make(weights=(1,2)).coverage(['0']),make(weights=(10,20)).coverage(['0']))
    def test_shared_candidate_gain(self):
        self.assertEqual(make().marginal(['0'],'1')['m'], {'lower':0., 'upper':.4})
    def test_independent_gain(self):
        gain=make(same=False).marginal(['0'],'1')['m']
        self.assertAlmostEqual(gain['lower'],.2)
        self.assertAlmostEqual(gain['upper'],.2)
    def test_bounds_against_enumerated_joint_distributions(self):
        # Exhaustive 3-event joint probabilities from deterministic reproducible draws.
        import random
        rng=random.Random(9)
        states=list(itertools.product((0,1),repeat=3))
        for _ in range(100):
            raw=[rng.random() for _ in states]; probs=[x/sum(raw) for x in raw]
            marg=[sum(p for state,p in zip(states,probs) if state[j]) for j in range(3)]
            audit=make(tuple(marg))
            union=sum(p for state,p in zip(states,probs) if any(state))
            b=audit.coverage(['0','1','2'])['m']
            self.assertLessEqual(b['lower'],union+1e-12); self.assertGreaterEqual(b['upper'],union-1e-12)
            gain=sum(p for state,p in zip(states,probs) if state[2] and not(state[0] or state[1]))
            b=audit.marginal(['0','1'],'2')['m']
            self.assertLessEqual(b['lower'],gain+1e-12); self.assertGreaterEqual(b['upper'],gain-1e-12)
    def test_ra_wrap(self): self.assertAlmostEqual(angular_separation(359,0,1,0),2)
    def test_pole(self): self.assertAlmostEqual(angular_separation(0,90,180,90),0)
    def test_antipodes(self): self.assertAlmostEqual(angular_separation(0,0,180,0),180)
    def test_bad_coordinate(self):
        with self.assertRaises(ValueError): angular_separation(0,91,0,0)
