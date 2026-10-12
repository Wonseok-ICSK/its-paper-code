"""Synthetic-data checks; these do not reproduce the original research results."""
import contextlib
import importlib.util
import io
from pathlib import Path
import unittest
import pandas as pd
import runpy
import sys
import types
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('traffic_helpers', ROOT / 'src' / 'cv.py')
cv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cv)


class ReviewFixTests(unittest.TestCase):
    def test_trapezoidal_delay_matches_known_area(self):
        self.assertAlmostEqual(cv.measureDelay(0, 3, [0, 2, 4], [0, 0, 0]), 4.0)

    def data(self, preceding_speed):
        return pd.DataFrame([
            dict(id=1, frame=25, precedingId=2, leftPrecedingId=0, rightPrecedingId=0, xVelocity=5.0),
            dict(id=2, frame=25, precedingId=0, leftPrecedingId=0, rightPrecedingId=0, xVelocity=preceding_speed),
        ])

    def test_stationary_preceding_vehicle_does_not_divide_by_zero(self):
        for fn in (cv.detectSlowVeh, cv.detectSlowVehPandas):
            with self.subTest(function=fn.__name__), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(fn(self.data(0.0)), [])

    def test_missing_preceding_observation_is_skipped(self):
        data = self.data(10.0).iloc[:1]
        for fn in (cv.detectSlowVeh, cv.detectSlowVehPandas):
            with self.subTest(function=fn.__name__), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(fn(data), [])

    def test_moving_preceding_vehicle_still_classifies_candidate(self):
        for fn in (cv.detectSlowVeh, cv.detectSlowVehPandas):
            with self.subTest(function=fn.__name__), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(fn(self.data(10.0)), [1])

    def test_unsorted_metadata_preserves_the_latest_frame(self):
        plot = types.ModuleType('matplotlib.pyplot')
        plot.rcParams = {}
        for name in ('figure', 'title', 'xlabel', 'ylabel', 'xlim', 'ylim', 'plot', 'savefig'):
            setattr(plot, name, Mock())
        progress = types.ModuleType('tqdm')
        progress.tqdm = lambda items, **kwargs: items
        table = pd.DataFrame({'frame': [0, 25, 50], 'id': [1, 1, 1]})
        metadata = 'id,a,b,c,finalFrame\n1,0,0,0,50\n2,0,0,0,25\n'
        with patch.dict(sys.modules, {'matplotlib.pyplot': plot, 'tqdm': progress}), \
                patch('matplotlib.pyplot', plot), \
                patch('builtins.open', side_effect=lambda *a, **k: io.StringIO(metadata)), \
                patch('pandas.read_csv', return_value=table):
            runpy.run_path(str(ROOT / 'src' / 'countVehicle_inFrame.py'))
        self.assertEqual(plot.xlim.call_args.args, (0, 2))
        self.assertEqual(plot.plot.call_args.args[0], [1, 1, 1])


if __name__ == '__main__':
    unittest.main()
