from unittest import TestCase

import sys
sys.path.append("../")
from Enchain import run_main


class TestMainWindow(TestCase):

	app = None
	mwin = None

	def setUp(self):
		self.app, self.mwin = run_main()

	def tearDown(self):
		self.mwin.close()
		self.app.quit()

	def test_noop(self):
		pass

