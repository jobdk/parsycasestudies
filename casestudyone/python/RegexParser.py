from parsy import Parser, forward_declaration, regex, string, whitespace, seq

from casestudyone.python.Constants import Constants
from casestudyone.python.SemanticModelBuilder import SemanticModelBuilder


class RegexParser:
    quantification_pattern: Parser = regex('(\\d+)\\.\\.(\\d+)').desc(
        'a correct quantification pattern such as 1..2 with only positive values and in correct order')

    occurs_parser = string(" occurs ")
    indefinitely_parser = regex('indefinitely').result(Constants.INDEFINITELY)
    quantification_parser: Parser = occurs_parser.then(
        indefinitely_parser | quantification_pattern.mark().map(lambda x: SemanticModelBuilder.
                                                                build_quantification(x[0], x[1], x[2])))

    term_pattern: Parser = regex('"[^"]+"').desc('term surrounded by double quotes e.g "hello world"')
    term_parser: Parser = seq(term_pattern, quantification_parser.optional()).combine(lambda term, quantification:
                                                                                      SemanticModelBuilder.build_single_term(
                                                                                          SemanticModelBuilder.map_term(
                                                                                              term), quantification))

    anything_parser: Parser = string("anything").result(Constants.ANYTHING_PATTERN)
    something_parser: Parser = string("something").result(Constants.SOMETHING_PATTERN)
    letters_parser: Parser = string("letters").result(Constants.ANY_LETTERS_PATTERN)
    numbers_parser: Parser = string("numbers").result(Constants.ANY_NUMBER_PATTERN)
    predefined_terms_parser: Parser = anything_parser | something_parser | letters_parser | numbers_parser

    new_line_opt_parser: Parser = string('\n').desc('new line').optional()
    whitespace_opt_parser: Parser = whitespace.desc('whitespace').optional()

    inner_regex_parser: forward_declaration = forward_declaration()

    or_parser: Parser = whitespace.optional().then(string('or')).skip(
        whitespace.optional())
    split_by_or_parser: Parser = Parser.sep_by(inner_regex_parser | predefined_terms_parser | term_parser, or_parser)

    starts_with_parser: Parser = string("starts with ").then(split_by_or_parser.map(
        lambda content: SemanticModelBuilder.starts_with_builder(content))).skip(new_line_opt_parser)

    followed_with_parser: Parser = whitespace_opt_parser.then(
        string("followed with ")).then(split_by_or_parser.map(
        lambda content: SemanticModelBuilder.followed_with_builder(content))).skip(new_line_opt_parser)

    ends_with_parser: Parser = string("ends with ").then(split_by_or_parser.map(
        lambda content: SemanticModelBuilder.ends_with_builder(content))).skip(new_line_opt_parser)

    inner_regex_parser.become(
        string('inner regex(').desc(
            'inner regex(followed with "Example" followed with "Example2")').then(followed_with_parser.many())
        .skip(string(')')))

    regex_parser: Parser = seq(whitespace_opt_parser.then(
        starts_with_parser.optional()),
        whitespace_opt_parser.then(followed_with_parser.many().optional()),
        whitespace_opt_parser.then(ends_with_parser.optional())
    ).combine(
        lambda starts_with_opt, followed_with_opt, ends_with_opt:
        SemanticModelBuilder
        .build_regex(starts_with_opt, followed_with_opt, ends_with_opt))
