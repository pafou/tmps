import unittest
import os
import json
from tmps_package.tmps_mod import Tmps, tmps_error

class TestTmps(unittest.TestCase):

    def setUp(self):
        # Create a temporary environment for testing
        self.env = "test_env"
        self.tmps = Tmps(self.env)

    def tearDown(self):
        # Clean up the temporary environment after tests
        import shutil
        test_dir = os.path.join('/tmp/tmps', self.env)
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_init(self):
        # Test that the environment directory is created
        test_dir = os.path.join('/tmp/tmps', self.env)
        self.assertTrue(os.path.exists(test_dir))

    def test_json_read_valid(self):
        # Test that json_read correctly parses valid JSON
        valid_json = '{"env": "test_env", "mode": "0644", "name": "test_file"}'
        self.tmps.json_read(valid_json)
        self.assertEqual(self.tmps.name, "test_file")
        self.assertEqual(self.tmps.mode, "0644")

    def test_json_read_invalid_env(self):
        # Test that json_read raises an error for invalid environment
        invalid_json = '{"env": "invalid_env", "mode": "0644", "name": "test_file"}'
        with self.assertRaises(SystemExit) as cm:
            self.tmps.json_read(invalid_json)
        self.assertEqual(cm.exception.code, 1)

    def test_json_read_invalid_mode(self):
        # Test that json_read raises an error for invalid mode
        invalid_json = '{"env": "test_env", "mode": "0888", "name": "test_file"}'
        with self.assertRaises(SystemExit) as cm:
            self.tmps.json_read(invalid_json)
        self.assertEqual(cm.exception.code, 1)

    def test_json_read_invalid_name(self):
        # Test that json_read raises an error for invalid name
        invalid_json = '{"env": "test_env", "mode": "0644", "name": "invalid@name"}'
        with self.assertRaises(SystemExit) as cm:
            self.tmps.json_read(invalid_json)
        self.assertEqual(cm.exception.code, 1)

    def test_post(self):
        # Test that post creates a new file
        json_data = '{"env": "test_env", "mode": "0644", "name": "test_file"}'
        self.tmps.post(json_data)
        test_file_path = os.path.join('/tmp/tmps', self.env, 'test_file')
        self.assertTrue(os.path.exists(test_file_path))

    def test_post_file_exists(self):
        # Test that post raises an error if file already exists
        json_data = '{"env": "test_env", "mode": "0644", "name": "test_file"}'
        self.tmps.post(json_data)
        with self.assertRaises(SystemExit) as cm:
            self.tmps.post(json_data)
        self.assertEqual(cm.exception.code, 1)

    def test_put(self):
        # Test that put updates an existing file
        # First create the file
        json_data = '{"env": "test_env", "mode": "0644", "name": "test_file"}'
        self.tmps.post(json_data)
        # Then update it
        update_json = '{"env": "test_env", "mode": "0755", "name": "test_file"}'
        self.tmps.put("test_file", update_json)
        test_file_path = os.path.join('/tmp/tmps', self.env, 'test_file')
        self.assertTrue(os.path.exists(test_file_path))
        # Check the mode was updated
        mode = os.stat(test_file_path).st_mode
        self.assertEqual(oct(mode), '0o100755')

    def test_put_file_not_exist(self):
        # Test that put raises an error if file doesn't exist
        update_json = '{"env": "test_env", "mode": "0755", "name": "non_existent_file"}'
        with self.assertRaises(SystemExit) as cm:
            self.tmps.put("non_existent_file", update_json)
        self.assertEqual(cm.exception.code, 1)

    def test_delete(self):
        # Test that delete removes an existing file
        json_data = '{"env": "test_env", "mode": "0644", "name": "test_file"}'
        self.tmps.post(json_data)
        test_file_path = os.path.join('/tmp/tmps', self.env, 'test_file')
        self.assertTrue(os.path.exists(test_file_path))
        self.tmps.delete("test_file")
        self.assertFalse(os.path.exists(test_file_path))

    def test_delete_file_not_exist(self):
        # Test that delete raises an error if file doesn't exist
        with self.assertRaises(SystemExit) as cm:
            self.tmps.delete("non_existent_file")
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
