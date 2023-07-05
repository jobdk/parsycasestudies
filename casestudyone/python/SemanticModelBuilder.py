from casestudyone.python.Constants import Constants
from casestudyone.python.SemanticError import SemanticError


class SemanticModelBuilder:

    @staticmethod
    def build_single_term(content, quantification) -> str:
        if quantification is not None:
            return f"({content}){quantification}"
        return content

    @staticmethod
    def build_quantification(
            start: tuple, quantification: str, end: tuple) \
            -> str:
        first, last = quantification.split('..')
        SemanticModelBuilder.validate_quantification_order(
            start, first, last, end)
        if first == last:
            return f"{{{first}}}"
        return f"{{{first},{last}}}"

    @staticmethod
    def validate_quantification_order(start: tuple, first: str, last, end: tuple):
        if int(first) > int(last):
            raise SemanticError(
                "Invalid quantification order. First number "
                "must be smaller than the second number for {0}..{1} between {2} and {3}.".format(
                    first, last, str(start), str(end)))

    @staticmethod
    def starts_with_builder(content) -> str:
        result = [str(item) if not isinstance(item, list) else str(item[0]) for item in content]
        return "^({0})".format(Constants.OR_SYMBOL_DELIMITER.join(result))

    @staticmethod
    def followed_with_builder(content) -> str:
        result = ''
        if any(isinstance(element, list) for element in content):
            for (element) in content:
                if isinstance(element, str):
                    result += element + '|'
                if isinstance(element, list):
                    result += ''.join(element)
            return "({0})".format(result)
        return "({0})".format(Constants.OR_SYMBOL_DELIMITER.join(content))

    @staticmethod
    def ends_with_builder(content) -> str:
        result = [str(item) if not isinstance(item, list) else str(item[0]) for item in content]
        return "({0})$".format(Constants.OR_SYMBOL_DELIMITER.join(result))

    @staticmethod
    def build_regex(starts_with_opt: str, followed_with_opt: list[str], ends_with_opt: str) -> str:
        result: str = ""
        if starts_with_opt is not None:
            result += starts_with_opt
        if followed_with_opt is not None:
            result += ''.join(followed_with_opt)
        if ends_with_opt is not None:
            result += ends_with_opt
        return result

    @staticmethod
    def map_term(content: str):
        return content[1:-1].replace(".", "\\.")
