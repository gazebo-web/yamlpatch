import os
import unittest

from yamlpath import YAMLPath
from main import run, load_file, setup_logger, setup_editor, setup_processor


class GenerateConfigYAML(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("./examples/local")
        self.logger = setup_logger()
        self.editor = setup_editor()

    def test_config_file_generated(self):
        run()
        self.assertTrue(os.path.exists("config.yaml"))

    def test_version_changed_second_patch(self):
        run()
        content = load_file(self.editor, self.logger, "config.yaml")
        config = setup_processor(self.logger, content)
        nodes = config.get_nodes(YAMLPath("version"))
        v = next(nodes, "")

        # It should not be empty
        self.assertNotEqual(v, "")

        # It should not be 1.0 neither 1.1
        self.assertNotEqual(v.node, "1.0")
        self.assertNotEqual(v.node, "1.1")

        # It should be 1.2
        self.assertEqual(v.node, "1.2")

    def test_added_field_exists(self):
        run()

        content = load_file(self.editor, self.logger, "config.yaml")
        config = setup_processor(self.logger, content)
        nodes = config.get_nodes(YAMLPath("spec.added"))
        v = next(nodes, "")

        # It should not be empty
        self.assertNotEqual(v, "")

        # It should contain the patch value
        self.assertEqual(v.node, "patch")

    def tearDown(self) -> None:
        if os.path.exists("config.yaml"):
            os.remove("config.yaml")
        os.chdir("../..")


if __name__ == '__main__':
    unittest.main()
