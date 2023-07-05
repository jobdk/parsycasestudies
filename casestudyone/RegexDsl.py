from parsy import *


class RegexParser:
    delimiter_occurs = " occurs "
    delimiter_or = " or "

    sentenceParser: Parser = regex('"[^"]+"').map(
        lambda x: SemanticModelBuilder.remove_double_quotes(x))
    multiplicityParser: Parser = regex('(\\d+)\\.\\.(\\d+)').map(
        lambda x: SemanticModelBuilder.build_multiplicity(x))
    anythingParser: Parser = regex('"anything"').map(lambda x: Constants.ANYTHING_PATTERN)
    somethingParser: Parser = regex('"something"').map(lambda x: Constants.SOMETHING_PATTERN)
    lettersParser: Parser = regex('"letters"').map(lambda x: Constants.ANY_LETTERS_PATTERN)
    numbersParser: Parser = regex('"numbers"').map(lambda x: Constants.ANY_NUMBER_PATTERN)
    literalsParser: Parser = anythingParser | somethingParser | lettersParser | numbersParser

    indefinitelyParser: Parser = regex('"indefinitely"')  # todo

    delimiterOccursParser: Parser = Parser.sep_by(literalsParser | multiplicityParser | sentenceParser,
                                                  string(delimiter_occurs))

    # returns a string
    orSplitParser: Parser = Parser.sep_by(delimiterOccursParser, string(delimiter_or))

    starts_with_parser: Parser = string("starts with ") >> orSplitParser.map(
        lambda content: SemanticModelBuilder.starts_with_builder(content))
    follows_with_parser: Parser = string("followed with ") >> orSplitParser.map(
        lambda content: SemanticModelBuilder.follows_with_builder(content))
    ends_with_parser: Parser = string("ends with ") >> orSplitParser.map(
        lambda content: SemanticModelBuilder.ends_with_builder(content))

    patternParser = seq(
        starts_with_parser.optional(),
        follows_with_parser.optional(),
        ends_with_parser.optional()
    ).combine(
        lambda starts_with_opt, followed_with_opt, ends_with_opt:
        SemanticModelBuilder.build_regex(starts_with_opt, followed_with_opt, ends_with_opt))


# todo: ends with
class SemanticModelBuilder:
    @staticmethod
    def build_multiplicity(x: str) -> str:
        multiplicity: list[str] = x.split('..')
        result = '{' + multiplicity[0] + ',' + multiplicity[1] + '}'
        return result

    @staticmethod
    def starts_with_builder(content: list[list[str]]) -> str:
        result: list[str] = []
        for x in content:
            if len(x) == 2:
                result.append('(' + x[0] + ')' + x[1])
            else:
                result.append(x[0])
        return "^({0})".format(Constants.or_delimiter.join(result))

    @staticmethod
    def ends_with_builder(content: list[list[str]]) -> str:
        result: list[str] = []
        for x in content:
            if len(x) == 2:
                result.append('(' + x[0] + ')' + x[1])
            else:
                result.append(x[0])
        return "({0})$".format(Constants.or_delimiter.join(result))

    @staticmethod
    def follows_with_builder(content: list[list[str]]) -> str:
        result: list[str] = []
        for x in content:
            if len(x) == 2:
                result.append('(' + x[0] + ')' + x[1])
            else:
                result.append(x[0])
        return "({0})".format(Constants.or_delimiter.join(result))


    @staticmethod
    def build_regex(starts_with_opt: str, followed_with_opt: str, ends_with_opt: str) -> str:
        result = ""
        if starts_with_opt is not None:
            result += starts_with_opt
        if followed_with_opt is not None:
            result += followed_with_opt
        if ends_with_opt is not None:
            result += ends_with_opt
        return result

    @staticmethod
    def remove_double_quotes(content: str) -> str:
        return content.replace('"', '')


class Constants:
    or_delimiter: str = '|'
    ANYTHING = "anything"
    SOMETHING = "something"
    ANY_LETTERS = "letters"
    ANY_NUMBER = "numbers"
    INDEFINITELY = "indefinitely"
    ANYTHING_PATTERN = ".*"
    SOMETHING_PATTERN = ".+"
    ANY_LETTERS_PATTERN = r"[a-zA-ZäÄüÜöÖß\s]+"
    ANY_NUMBER_PATTERN = r"[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?"

# todo:
#  - starts should work -> done
#  - following should work
#  - ends should work
#  - or
#  - remove double quotes
