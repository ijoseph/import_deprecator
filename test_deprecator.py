import unittest
import warnings


class TestDeprecator(unittest.TestCase):
    def setUp(self):
        # print warnings by default
        warnings.simplefilter("always")

    def test_deprecate(self):
        # import library_module

        # 'foo' is not deprecated; ensure does not warn, as would throw exception
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            from library_module import replacement

        # 'bar' is deprecated, warns
        with warnings.catch_warnings(record=True) as w:
            from library_module import previous_name

            self.assertTrue(len(w) > 0)
            self.assertIn(
                "'library_module.previous_name' has been renamed", str(w[0])
            )
            # old function still works, though:
            self.assertEqual("new function result", previous_name())

            # as does new function
            from library_module import replacement

            self.assertIn("new function result", replacement())


if __name__ == "__main__":
    unittest.main()
