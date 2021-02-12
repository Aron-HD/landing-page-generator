import unittest
from context import sample
from sample.core import get_csv

class TestStringMethods(unittest.TestCase):

	def test1(self):
		result = get_csv(cat='asia',csv='judges')
		self.assertTrue(result)

	def test2(self):
		pass

if __name__ == '__main__':
	unittest.main()
