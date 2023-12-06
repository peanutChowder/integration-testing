# tests/TestRunner.py
#The basic idea here is to have a new Python file Testrunner.py
# alongside your tests that contains our runner.
import unittest

# # import your tests modules (Apply integration testing method)
from tests_bottomup import TestModuleA
from tests_bottomup import TestModuleB
from tests_bottomup import TestModuleC
from tests_bottomup import TestModuleD
from tests_bottomup import TestModuleE
from tests_bottomup import TestModuleF
from tests_bottomup import TestModuleG



# # initialize the tests suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# # add tests to the tests suite
suite.addTests(loader.loadTestsFromModule(TestModuleA))
suite.addTests(loader.loadTestsFromModule(TestModuleB))
suite.addTests(loader.loadTestsFromModule(TestModuleC))
suite.addTests(loader.loadTestsFromModule(TestModuleD))
suite.addTests(loader.loadTestsFromModule(TestModuleE))
suite.addTests(loader.loadTestsFromModule(TestModuleF))
suite.addTests(loader.loadTestsFromModule(TestModuleG))


# # initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)