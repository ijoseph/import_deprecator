import unittest
import warnings


class TestDeprecator(unittest.TestCase):
    def setUp(self):
        # print warnings by default
        warnings.simplefilter("always")

    def test_deprecate(self):

        import deprecator

        deprecator.modify_imports()

        # 'foo' is not deprecated; ensure does not warn, as would throw exception
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            from library_module import foo

        # 'bar' is deprecated, warns
        with warnings.catch_warnings(record=True) as w:
            from library_module import bar

            self.assertTrue(len(w) > 0)


if __name__ == "__main__":
    unittest.main()
