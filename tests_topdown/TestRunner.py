import unittest

# import your tests modules (Apply integration testing method)
from tests_topdown import TestModuleA
from tests_topdown import TestModulesABCDE
from tests_topdown import TestModulesABCDEFG



# initialize the tests suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the tests suite
suite.addTests(loader.loadTestsFromModule(TestModuleA))
suite.addTests(loader.loadTestsFromModule(TestModulesABCDE))
suite.addTests(loader.loadTestsFromModule(TestModulesABCDEFG))


# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)