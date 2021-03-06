#!/usr/bin/env python

from __future__ import print_function, division
import bayesloop as bl
import numpy as np


class ParameterParsing:
    def test_inequality(self):
        S = bl.Study()
        S.loadData(np.array([1, 2, 3, 4, 5]))
        S.setOM(bl.om.Poisson('rate', bl.oint(0, 6, 50)))
        S.setTM(bl.tm.Static())
        S.fit()

        S2 = bl.Study()
        S2.loadData(np.array([1, 2, 3, 4, 5]))
        S2.setOM(bl.om.Poisson('rate2', bl.oint(0, 6, 50)))
        S2.setTM(bl.tm.GaussianRandomWalk('sigma', 0.2, target='rate2'))
        S2.fit()

        P = bl.Parser(S, S2)
        P('log(rate2*2*1.2) + 4 + rate^2 > 20', t=3)
        np.testing.assert_almost_equal(P('log(rate2@1*2*1.2) + 4 + rate@2^2 > 20'), 0.162262091093, decimal=5,
                                       err_msg='Erroneous parsing result for inequality.')
        np.testing.assert_almost_equal(P('log(rate2*2*1.2) + 4 + rate^2 > 20', t=3), 0.163699467863, decimal=5,
                                       err_msg='Erroneous parsing result for inequality with fixed timestamp.')

    def test_distribution(self):
        S = bl.Study()
        S.loadData(np.array([1, 2, 3, 4, 5]))
        S.setOM(bl.om.Poisson('rate', bl.oint(0, 6, 50)))
        S.setTM(bl.tm.Static())
        S.fit()

        S2 = bl.Study()
        S2.loadData(np.array([1, 2, 3, 4, 5]))
        S2.setOM(bl.om.Poisson('rate2', bl.oint(0, 6, 50)))
        S2.setTM(bl.tm.GaussianRandomWalk('sigma', 0.2, target='rate2'))
        S2.fit()

        P = bl.Parser(S, S2)
        x, p = P('log(rate2@1*2*1.2)+ 4 + rate@2^2')
        np.testing.assert_allclose(p[100:105],
                                   [0.00643873, 0.00618468, 0.00466452, 0.00314371, 0.00365816],
                                   rtol=1e-05, err_msg='Erroneous derived probability distribution.')
