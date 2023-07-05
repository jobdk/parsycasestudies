import unittest

from casestudyone.RegexDsl import *


class MyTestCase(unittest.TestCase):
    # Starts with
    def test_starts_with_anything(self):
        regex_dsl = 'starts with "anything"'
        result = RegexParser.patternParser.parse(regex_dsl)
        self.assertEqual(result, '^({0})'.format(Constants.ANYTHING_PATTERN))
        self.assertTrue(re.match(result, '2424234.232'))
        self.assertTrue(re.match(result, 'Hello'))
        self.assertTrue(re.match(result, ''))

    def test_starts_with_something(self):
        regex_dsl = 'starts with "something"'
        result = RegexParser.patternParser.parse(regex_dsl)
        self.assertEqual(result, '^({0})'.format(Constants.SOMETHING_PATTERN))
        self.assertTrue(re.match(result, '2424234.232'))
        self.assertTrue(re.match(result, 'Hello'))
        self.assertFalse(re.match(result, ''))

    def test_starts_with_letters(self):
        regex_dsl = 'starts with "letters"'
        result = RegexParser.patternParser.parse(regex_dsl)
        self.assertEqual(result, '^({0})'.format(Constants.ANY_LETTERS_PATTERN))
        self.assertTrue(re.match(result, 'djkfhdsakfhs'))
        self.assertFalse(re.match(result, '232'))

    def test_starts_with_numbers(self):  # todo
        regex_dsl = 'starts with "numbers"'
        result = RegexParser.patternParser.parse(regex_dsl)
        self.assertEqual(result, '^({0})'.format(Constants.ANY_NUMBER_PATTERN))
        self.assertTrue(re.match(result, '2424234.232'))
        self.assertFalse(re.match(result, 'Hello'))

    def test_starts_with_hello(self):
        regex_dsl = 'starts with "Hello"'
        result = RegexParser.patternParser.parse(regex_dsl)
        self.assertEqual(result, '^(Hello)')
        self.assertTrue(re.match(result, 'Hello'))
        self.assertFalse(re.match(result, 'hello'))

    #
    def test_starts_with_At(self):
        regex_dsl = 'starts with "@"'
        result = RegexParser.patternParser.parse(regex_dsl)
        self.assertEqual(result, '^(@)')
        self.assertTrue(re.match(result, '@'))

    def test_starts_with_first_or_second(self):
        regex_dsl = 'starts with "first" or "second"'
        result = RegexParser.patternParser.parse(regex_dsl)
        self.assertEqual(result, '^(first|second)')
        self.assertTrue(re.match(result, "first"))
        self.assertTrue(re.match(result, "second"))
        self.assertFalse(re.match(result, "third"))
        self.assertFalse(re.match(result, "fist"))

    def test_starts_with_white_space_between_words(self):
        regex_dsl = 'starts with "Hello World!" or "Hello"'
        result = RegexParser.patternParser.parse(regex_dsl)
        self.assertEqual(result, '^(Hello World!|Hello)')
        self.assertTrue(re.match(result, "Hello World!"))
        self.assertTrue(re.match(result, "Hello"))
        self.assertFalse(re.match(result, "Heldlo"))

    # ______followed with______
    def test_followed_with_anything(self):
        regex_dsl = 'followed with "anything"'
        result = RegexParser.patternParser.parse(regex_dsl)
        self.assertEqual(result, '({0})'.format(Constants.ANYTHING_PATTERN))
        self.assertTrue(re.match(result, '2424234.232'))
        self.assertTrue(re.match(result, 'Hello'))
        self.assertTrue(re.match(result, ''))
    # Multiplicity
    def test_starts_with_multiplicity(self):
        regex_dsl = 'starts with "aa" occurs 1..2 or "b" occurs 3..3'
        result = RegexParser.patternParser.parse(regex_dsl)
        self.assertEqual(result, '^((aa){1,2}|(b){3,3})')
        self.assertTrue(re.match(result, "aa"))
        self.assertTrue(re.match(result, "aaaa"))
        self.assertTrue(re.match(result, "bbb"))
        self.assertFalse(re.match(result, "abaa"))
        self.assertFalse(re.match(result, "bb"))
        self.assertFalse(re.match(result, "b"))

    def test_followed_with_multiplicity(self):
        regex_dsl = 'followed with "gmail" occurs 1..2 or "gmx" ' \
                    'followed with "." occurs 3..3 ' \
                    'followed with "com" or "de"'
        result = RegexParser.patternParser.parse(regex_dsl)
        self.assertEqual(result, '((gmail){1,2}|gmx)((\\.){3,3})(com|de)')
        self.assertTrue(re.match(result, "gmailgmail...com"))
        self.assertTrue(re.match(result, "gmail...de"))
        self.assertTrue(re.match(result, "gmx...com"))
        self.assertTrue(re.match(result, "gmx...de"))
        self.assertFalse(re.match(result, "gmxde"))
        self.assertFalse(re.match(result, "gmailgmx.de"))
        self.assertFalse(re.match(result, "gmail."))
        self.assertFalse(re.match(result, "gmail."))

    def test_ends_with_multiplicity(self):
        regex_dsl = 'ends with "aa" occurs 1..2 or "b" occurs 3..3'
        result = RegexParser.patternParser.parse(regex_dsl)
        self.assertEqual(result, '((aa){1,2}|(b){3,3})$')
        self.assertTrue(re.match(result, "aa"))
        self.assertTrue(re.match(result, "aaaa"))
        self.assertTrue(re.match(result, "bbb"))
        self.assertFalse(re.match(result, "aaa"))
        self.assertFalse(re.match(result, "bb"))
        self.assertFalse(re.match(result, "b"))

    # def test_starts_with_multiplicity_indefinitely(self):
    #     regex_dsl = 'ends with "aa" occurs indefinitely or "b" occurs 3..3'
    #     result = RegexParser.patternParser.parse(regex_dsl)
    #     self.assertEqual(result, '((aa)*|(b){3,3})$')
    #     self.assertTrue(re.match(result, "aaaaaaaaaa"))
    #     self.assertTrue(re.match(result, "aaaa"))
    #     self.assertTrue(re.match(result, "bbb"))
    #     self.assertFalse(re.match(result, "aaa"))
    #     self.assertFalse(re.match(result, "bb"))
    #     self.assertFalse(re.match(result, "b"))


if __name__ == '__main__':
    unittest.main()
