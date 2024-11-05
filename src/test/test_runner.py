import os
import sys
import unittest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

test_loader = unittest.TestLoader()
test_suite = test_loader.discover(
    os.path.join(os.path.dirname(__file__), 'localtestingsuites'),
    pattern='*_test.py'
)

runner = unittest.TextTestRunner(verbosity=2)
runner.run(test_suite)