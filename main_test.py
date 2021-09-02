import os
import unittest

from main import run


class GenerateConfigYAML(unittest.TestCase):
    def test_config_file_generated(self):
        os.chdir("./examples/local")
        run()
        self.assertTrue(os.path.isfile('config.yaml'), "config.yaml must exist")


if __name__ == '__main__':
    unittest.main()
