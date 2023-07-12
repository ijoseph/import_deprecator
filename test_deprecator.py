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
            from library_module import new_function

        # 'bar' is deprecated, warns
        with warnings.catch_warnings(record=True) as w:
            from library_module import deprecated_function
            self.assertTrue(len(w) > 0)
            self.assertIn("'library_module.deprecated_function' has been renamed", str(w[0]))
            # old function still works, though:
            self.assertEqual("new function result", deprecated_function())

            # as does new function
            from library_module import new_function
            self.assertIn("new function result", new_function())


if __name__ == "__main__":
    unittest.main()
