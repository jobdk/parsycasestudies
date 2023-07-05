import re
import unittest

from casestudyone.python.Constants import Constants
from casestudyone.python.RegexParser import RegexParser


class MyTestCase(unittest.TestCase):
    # _________________ starts with  _________________
    def test_starts_with_anything(self):
        regex_dsl = 'starts with anything'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '^({0})'.format(Constants.ANYTHING_PATTERN))
        self.assertTrue(re.fullmatch(result, 'Should match.'))
        self.assertTrue(re.fullmatch(result, ''))

    def test_starts_with_something(self):
        regex_dsl = 'starts with something'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '^({0})'.format(Constants.SOMETHING_PATTERN))
        self.assertTrue(re.fullmatch(result, 'Should match.'))
        self.assertFalse(re.fullmatch(result, ''))

    def test_starts_with_letters(self):
        regex_dsl = 'starts with letters'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual('^({0})'.format(Constants.ANY_LETTERS_PATTERN), result)
        self.assertTrue(re.fullmatch(result, 'Should match'))
        self.assertFalse(re.fullmatch(result, '232'))

    def test_starts_with_numbers(self):
        regex_dsl = 'starts with numbers'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual('^({0})'.format(Constants.ANY_NUMBER_PATTERN), result)
        self.assertTrue(re.fullmatch(result, '123'))
        self.assertFalse(re.fullmatch(result, 'Test'))

    def test_starts_with_hello(self):
        regex_dsl = 'starts with "Hello"'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual('^(Hello)', result)
        self.assertTrue(re.fullmatch(result, 'Hello'))
        self.assertFalse(re.fullmatch(result, 'hello'))

    def test_starts_with_At(self):
        regex_dsl = 'starts with "@"'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '^(@)')
        self.assertTrue(re.fullmatch(result, '@'))

    def test_starts_with_first_or_second(self):
        regex_dsl = 'starts with "first" or "second"'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '^(first|second)')
        self.assertTrue(re.fullmatch(result, "first"))
        self.assertTrue(re.fullmatch(result, "second"))
        self.assertFalse(re.fullmatch(result, "third"))
        self.assertFalse(re.fullmatch(result, "fist"))

    def test_starts_with_white_space_between_words(self):
        regex_dsl = 'starts with "Hello World!" or "Hello"'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '^(Hello World!|Hello)')
        self.assertTrue(re.fullmatch(result, "Hello World!"))
        self.assertTrue(re.fullmatch(result, "Hello"))
        self.assertFalse(re.fullmatch(result, "Test"))

    # _________________ followed with  _________________
    def test_followed_with_anything(self):
        regex_dsl = 'followed with anything'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '({0})'.format(Constants.ANYTHING_PATTERN))
        self.assertTrue(re.fullmatch(result, 'Should match.'))
        self.assertTrue(re.fullmatch(result, ''))

    def test_followed_with_something(self):
        regex_dsl = 'followed with something'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '({0})'.format(Constants.SOMETHING_PATTERN))
        self.assertTrue(re.fullmatch(result, 'Should match.'))
        self.assertFalse(re.fullmatch(result, ''))

    def test_followed_with_letters(self):
        regex_dsl = 'followed with letters'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '({0})'.format(Constants.ANY_LETTERS_PATTERN))
        self.assertTrue(re.fullmatch(result, 'Should match'))
        self.assertFalse(re.fullmatch(result, '123'))

    def test_followed_with_numbers(self):
        regex_dsl = 'followed with numbers'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '({0})'.format(Constants.ANY_NUMBER_PATTERN))
        self.assertTrue(re.fullmatch(result, '123'))
        self.assertFalse(re.fullmatch(result, 'Test'))

    def test_followed_with_at(self):
        regex_dsl = 'followed with "@"'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, "(@)")
        self.assertTrue(re.fullmatch(result, "@"))
        self.assertFalse(re.fullmatch(result, "@@"))

    def test_followed_with_at_or_email(self):
        regex_dsl = 'followed with "@" or "email"'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, "(@|email)")
        self.assertTrue(re.fullmatch(result, "@"))
        self.assertTrue(re.fullmatch(result, "email"))
        self.assertFalse(re.fullmatch(result, "@email"))
        self.assertFalse(re.fullmatch(result, "emailtest"))

    def test_followed_with_multiple_times_in_correct_order(self):
        regex_dsl = '''followed with "gmail" or "gmx"
followed with "."
followed with "com" or "de"'''
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, "(gmail|gmx)(\\.)(com|de)")
        self.assertTrue(re.fullmatch(result, "gmail.com"))
        self.assertTrue(re.fullmatch(result, "gmail.de"))
        self.assertTrue(re.fullmatch(result, "gmx.com"))
        self.assertTrue(re.fullmatch(result, "gmx.de"))
        self.assertFalse(re.fullmatch(result, "gmxde"))
        self.assertFalse(re.fullmatch(result, "gmailgmx.de"))
        self.assertFalse(re.fullmatch(result, "gmail."))

    # _________________ ends with  _________________
    def test_ends_with_anything(self):
        regex_dsl = 'ends with anything'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '({0})$'.format(Constants.ANYTHING_PATTERN))
        self.assertTrue(re.fullmatch(result, 'Should match.'))
        self.assertTrue(re.fullmatch(result, ''))

    def test_ends_with_something(self):
        regex_dsl = 'ends with something'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '({0})$'.format(Constants.SOMETHING_PATTERN))
        self.assertTrue(re.fullmatch(result, 'Should match.'))
        self.assertFalse(re.fullmatch(result, ''))

    def test_ends_with_letters(self):
        regex_dsl = 'ends with letters'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '({0})$'.format(Constants.ANY_LETTERS_PATTERN))
        self.assertTrue(re.fullmatch(result, 'Should match'))
        self.assertFalse(re.fullmatch(result, '232'))

    def test_ends_with_numbers(self):
        regex_dsl = 'ends with numbers'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '({0})$'.format(Constants.ANY_NUMBER_PATTERN))
        self.assertTrue(re.fullmatch(result, '123'))
        self.assertFalse(re.fullmatch(result, 'Test'))

    def test_ends_with_hello(self):
        regex_dsl = 'ends with "Hello"'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '({0})$'.format("Hello"))
        self.assertTrue(re.fullmatch(result, 'Hello'))
        self.assertFalse(re.fullmatch(result, 'Hello World'))

    def test_ends_with_first_or_second(self):
        regex_dsl = 'ends with "first" or "second"'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '({0})$'.format("first|second"))
        self.assertTrue(re.fullmatch(result, "first"))
        self.assertTrue(re.fullmatch(result, "second"))
        self.assertFalse(re.fullmatch(result, "third"))
        self.assertFalse(re.fullmatch(result, "fourth"))

    # _________________ Multiplicities  _________________
    def test_starts_with_quantification(self):
        regex_dsl = 'starts with "aa" occurs 1..2 or "b" occurs 3..3'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual('^((aa){1,2}|(b){3})', result)
        self.assertTrue(re.fullmatch(result, "aa"))
        self.assertTrue(re.fullmatch(result, "aaaa"))
        self.assertTrue(re.fullmatch(result, "bbb"))
        self.assertFalse(re.fullmatch(result, "abaa"))
        self.assertFalse(re.fullmatch(result, "bb"))
        self.assertFalse(re.fullmatch(result, "b"))

    def test_followed_with_quantification(self):
        regex_dsl = '''followed with "gmail" occurs 1..2 or "gmx"
followed with "." occurs 3..3
followed with "com" or "de"'''
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '((gmail){1,2}|gmx)((\\.){3})(com|de)')
        self.assertTrue(re.fullmatch(result, "gmailgmail...com"))
        self.assertTrue(re.fullmatch(result, "gmail...de"))
        self.assertTrue(re.fullmatch(result, "gmx...com"))
        self.assertTrue(re.fullmatch(result, "gmx...de"))
        self.assertFalse(re.fullmatch(result, "gmxde"))
        self.assertFalse(re.fullmatch(result, "gmailgmx.de"))
        self.assertFalse(re.fullmatch(result, "gmail."))
        self.assertFalse(re.fullmatch(result, "gmail."))

    def test_ends_with_quantification(self):
        regex_dsl = 'ends with "aa" occurs 1..2 or "b" occurs 3..3'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '((aa){1,2}|(b){3})$')
        self.assertTrue(re.fullmatch(result, "aa"))
        self.assertTrue(re.fullmatch(result, "aaaa"))
        self.assertTrue(re.fullmatch(result, "bbb"))
        self.assertFalse(re.fullmatch(result, "aaa"))
        self.assertFalse(re.fullmatch(result, "bb"))
        self.assertFalse(re.fullmatch(result, "b"))

    def test_starts_with_quantification_indefinitely(self):
        regex_dsl = 'ends with "aa" occurs indefinitely or "b" occurs 3..3'
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '((aa)*|(b){3})$')
        self.assertTrue(re.fullmatch(result, "aaaaaaaaaa"))
        self.assertTrue(re.fullmatch(result, "aaaa"))
        self.assertTrue(re.fullmatch(result, "bbb"))
        self.assertFalse(re.fullmatch(result, "aaa"))
        self.assertFalse(re.fullmatch(result, "bb"))
        self.assertFalse(re.fullmatch(result, "b"))

    # ___________________ integration ____________________
    def test_simple_regex(self):
        regex_dsl = '''starts with "T"
followed with anything
ends with "s."'''
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '^(T)(.*)(s\.)$')
        self.assertTrue(re.fullmatch(result, 'This matches.'))
        self.assertFalse(re.fullmatch(result, 'This does not match.'))

    def test_simple_regex_2(self):
        regex_dsl = ''' starts with "This m"
            followed with "atche"
            ends with "s."'''
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '^(This m)(atche)(s\.)$')
        self.assertTrue(re.fullmatch(result, 'This matches.'))
        self.assertFalse(re.fullmatch(result, 'Does not match.'))

    def test_email_regex(self):
        # GIVEN
        regex_dsl = '''
        starts with something
        followed with "@"
        followed with something
        followed with "."
        ends with "com" or "de" or "net"'''

        # WHEN
        result = RegexParser.regex_parser.parse(regex_dsl)

        # THEN
        self.assertEqual(result, '^(.+)(@)(.+)(\\.)(com|de|net)$')
        self.assertTrue(re.fullmatch(result, 'name@gmail.com'))
        self.assertTrue(re.fullmatch(result, 'name@gmx.de'))
        self.assertTrue(re.fullmatch(result, 'name@gmx.de'))
        self.assertTrue(re.fullmatch(result, 'name@gmx.net'))
        self.assertFalse(re.fullmatch(result, '@gmx.de'))
        self.assertFalse(re.fullmatch(result, 'name@.de'))
        self.assertFalse(re.fullmatch(result, 'name@.ch'))
        self.assertFalse(re.fullmatch(result, 'name.de'))


    # _________________ inner regex _________________
    def test_inner_regex(self):
        regex_dsl = '''starts with inner regex(followed with "John" or "Steve") or "Hello"
        followed with "Doe" or "Mustermann"
        followed with "@"
        ends with "gmail.com"'''

        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual('^((John|Steve)|Hello)(Doe|Mustermann)(@)(gmail\.com)$', result)
        self.assertTrue(re.fullmatch(result, 'JohnDoe@gmail.com'))
        self.assertTrue(re.fullmatch(result, 'JohnMustermann@gmail.com'))
        self.assertTrue(re.fullmatch(result, 'SteveMustermann@gmail.com'))
        self.assertTrue(re.fullmatch(result, 'HelloMustermann@gmail.com'))
        self.assertFalse(re.fullmatch(result, 'JohnD@gmail.com'))
        self.assertFalse(re.fullmatch(result, 'Demian@gmail.com'))

    def test_inner_regex_2(self):
        regex_dsl = '''starts with inner regex(followed with "John")
      followed with "Doe" or "Mustermann"
      followed with inner regex(followed with "a" followed with "b" or "c")
      ends with "end"'''

        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual('^((John))(Doe|Mustermann)((a)(b|c))(end)$', result)
        self.assertTrue(re.fullmatch(result, 'JohnDoeabend'))
        self.assertTrue(re.fullmatch(result, 'JohnMustermannacend'))
        self.assertFalse(re.fullmatch(result, 'JohnMustermannaend'))

    def test_inner_regex_followed_with_with_alternative(self):
        regex_dsl = '''starts with inner regex(followed with "1" or "2") or "4"
      followed with inner regex(followed with "a" followed with "b" or "c")
      ends with "end"'''

        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual('^((1|2)|4)((a)(b|c))(end)$', result)
        self.assertTrue(re.fullmatch(result, '1abend'))
        self.assertTrue(re.fullmatch(result, '2abend'))
        self.assertTrue(re.fullmatch(result, '4acend'))
        self.assertFalse(re.fullmatch(result, '4aend'))

    # ___________________ semantic validation ____________________
    def test_quantification_must_be_positive(self):
        # GIVEN
        error_message = 'expected one of \'a correct quantification pattern such as 1..2 with only positive values and in correct order\', \'indefinitely\' at 0:27'
        regex_dsl = 'starts with "first" occurs -1..1"'

        # WHEN
        with self.assertRaises(Exception) as context:
            RegexParser.regex_parser.parse(regex_dsl)
        print(str(context.exception))

        # THEN
        self.assertEqual(error_message, str(context.exception))

    def test_quantification_in_wrong_order(self):
        # GIVEN
        error_message = 'Invalid quantification order. First number must be smaller than the second number for 2..1 between (0, 27) and (0, 31).'
        regex_dsl = 'starts with "first" occurs 2..1'

        # WHEN
        with self.assertRaises(Exception) as context:
            RegexParser.regex_parser.parse(regex_dsl)
        print(str(context.exception))

        # THEN
        self.assertEqual(error_message, str(context.exception))

    def test_occurs_wrong_working_quantification(self):
        # GIVEN
        error_message = 'expected one of \'a correct quantification pattern such as 1..2 with only positive values and in correct order\', \'indefinitely\' at 0:24'
        regex_dsl = 'starts with "aa" occurs 2.1 or "b" occurs 3..3'

        # WHEN
        with self.assertRaises(Exception) as context:
            RegexParser.regex_parser.parse(regex_dsl)
        print(str(context.exception))

        # THEN
        self.assertEqual(error_message, str(context.exception))

    # --------------- Parser Combinator specific ---------------
    # Default error messages are already very good.
    def test_missing_pre_keyword(self):
        # GIVEN
        error_message_1 = 'expected one of \'EOF\', \'ends with \', \'followed with \', \'starts with \', \'whitespace\' at 0:0'
        regex_dsl = '''"4" or "5"'''

        # WHEN
        with self.assertRaises(Exception) as context:
            RegexParser.regex_parser.parse('''"4" or "5"''')
        print(str(context.exception))

        # THEN
        self.assertEqual(error_message_1, str(context.exception))

    def test_missing_pre_keywords_in_second_line(self):
        # GIVEN
        error_message = 'expected one of \'EOF\', \'ends with \', \'followed with \', \'or\', \'whitespace\' at 1:0'
        regex_dsl = '''starts with "4" or "5"
"6 3" or "7"'''

        # WHEN
        with self.assertRaises(Exception) as context:
            RegexParser.regex_parser.parse(regex_dsl)
        print(str(context.exception))

        # THEN
        self.assertEqual(error_message, str(context.exception))

    def test_wrong_pre_keyword_in_second_line(self):
        # GIVEN
        error_message = 'expected one of \'EOF\', \'ends with \', \'followed with \', \'or\', \'whitespace\' at 2:0'
        regex_dsl = '''starts with something
followed with "@"
folowed with something
ends with "com" or "de" or "net"'''

        # WHEN
        with self.assertRaises(Exception) as context:
            RegexParser.regex_parser.parse(regex_dsl)
        print(str(context.exception))

        # THEN
        self.assertEqual(error_message, str(context.exception))

    # --------------- Missing double quotes ---------------

    def test_missing_double_quotes_at_start_of_first(self):
        # GIVEN
        error_message = '''expected one of 'EOF', 'anything', 'ends with ', 'followed with ', 'inner regex(followed with "Example" followed with "Example2")', 'letters', 'new line', 'numbers', 'something', 'term surrounded by double quotes e.g "hello world"', 'whitespace' at 0:12'''
        regex_dsl = '''starts with 4" or "5"'''

        # WHEN
        with self.assertRaises(Exception) as context:
            RegexParser.regex_parser.parse(regex_dsl)
        print(str(context.exception))

        # THEN
        self.assertEqual(error_message, str(context.exception))

    def test_Missing_double_quotes_at_end_of_first(self):
        # GIVEN
        error_message = '''expected one of ' occurs ', 'EOF', 'ends with ', 'followed with ', 'new line', 'or', 'whitespace' at 0:19'''
        regex_dsl = '''starts with "4 or "5"'''

        with self.assertRaises(Exception) as context:
            # WHEN
            RegexParser.regex_parser.parse(regex_dsl)
        print(str(context.exception))

        # THEN
        self.assertEqual(error_message, str(context.exception))

    def test_missing_double_quote_at_start_of_second(self):
        # GIVEN
        error_message = '''expected one of 'anything', 'inner regex(followed with "Example" followed with "Example2")', 'letters', 'numbers', 'something', 'term surrounded by double quotes e.g "hello world"' at 0:19'''
        regex_dsl = '''starts with "4" or 5"'''

        # WHEN
        with self.assertRaises(Exception) as context:
            RegexParser.regex_parser.parse(regex_dsl)
        print(str(context.exception))

        # THEN
        self.assertEqual(error_message, str(context.exception))

    def test_missing_double_quote_at_end_of_second(self):
        # GIVEN
        error_message = '''expected one of 'anything', 'inner regex(followed with "Example" followed with "Example2")', 'letters', 'numbers', 'something', 'term surrounded by double quotes e.g "hello world"' at 0:19'''
        regex_dsl = '''starts with "4" or "5'''

        # WHEN
        with self.assertRaises(Exception) as context:
            RegexParser.regex_parser.parse(regex_dsl)
        print(str(context.exception))

        # THEN
        self.assertEqual(error_message, str(context.exception))

    def test_missing_all_double_quotes(self):
        # GIVEN
        error_message = '''expected one of 'EOF', 'anything', 'ends with ', 'followed with ', 'inner regex(followed with "Example" followed with "Example2")', 'letters', 'new line', 'numbers', 'something', 'term surrounded by double quotes e.g "hello world"', 'whitespace' at 0:12'''
        regex_dsl = '''starts with 4 or 5'''

        # WHEN
        with self.assertRaises(Exception) as context:
            RegexParser.regex_parser.parse(regex_dsl)
        print(str(context.exception))

        # THEN
        self.assertEqual(error_message, str(context.exception))

    # --------------- extra tests ---------------
    def test_or_inside_double_quotes_is_not_interpreted_as_splitting_term(self):
        regex_dsl = '''starts with "or" or "else" or "if"'''
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertEqual(result, '^(or|else|if)')
        self.assertTrue(re.fullmatch(result, 'or'))
        self.assertTrue(re.fullmatch(result, 'else'))
        self.assertTrue(re.fullmatch(result, 'if'))
        self.assertFalse(re.fullmatch(result, 'orelse'))
        self.assertFalse(re.fullmatch(result, 'Test'))

    def test_for_loc(self):
        regex_dsl = '''starts with "domain "
followed with inner regex(followed with "specific " followed with inner regex(followed with "modeling" or "design")) or "driven design"
ends with anything'''
        result = RegexParser.regex_parser.parse(regex_dsl)
        self.assertTrue(result, '^(domain )((specific )((modeling|design))|driven design)(.*)$')
        print(result)


if __name__ == '__main__':
    unittest.main()
