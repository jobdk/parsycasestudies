from parsy import Parser, string, seq, regex, whitespace

from casestudytwo.python.SemanticModel import NonAccessModifier, Access, Entity, DependencyType
from casestudytwo.python.SemanticModelBuilder import SemanticModelBuilder


class PlantUmlParser:
    whitespace_parser: Parser = whitespace.desc('whitespace')
    whitespace_opt_parser: Parser = whitespace_parser.optional()
    single_word_pattern: Parser = regex('\w+')

    open_bracket_parser: Parser = string("(").then(whitespace_opt_parser)
    closing_bracket_parser: Parser = string(")").then(whitespace_opt_parser)
    open_curly_braces_parser: Parser = whitespace_opt_parser >> string("{") << whitespace_opt_parser
    closing_curly_braces_parser: Parser = whitespace_opt_parser >> string("}") << whitespace_opt_parser

    abstract_parser: Parser = string('{abstract} ').result(NonAccessModifier.ABSTRACT)
    static_parser: Parser = string('{static} ').result(NonAccessModifier.STATIC)
    non_access_modifier_parser: Parser = abstract_parser | static_parser | string('').result(None)

    private_parser: Parser = string('- ').result(Access.private)
    public_parser: Parser = string('+ ').result(Access.public)
    protected_parser: Parser = string('# ').result(Access.protected)
    package_private_parser: Parser = string('~ ').result(Access.packagePrivate)
    access_parser: Parser = private_parser | public_parser | protected_parser | package_private_parser

    field_name_parser: Parser = single_word_pattern.desc('a single word as field name')
    type_parser: Parser = single_word_pattern.desc('a single word as type')
    method_name_parser: Parser = single_word_pattern.desc('a single word as method name')
    parameter_parser: Parser = seq(
        field_name_parser, whitespace_opt_parser, string(':'), whitespace_opt_parser, type_parser).combine(
        lambda name, whitespace_opt_1, split, whitespace_opt_2, type: SemanticModelBuilder.create_parameter(name, type))

    field_parser: Parser = seq(access_parser, non_access_modifier_parser, parameter_parser).combine(
        lambda access, non_access_modifier, parameter:
        SemanticModelBuilder.create_field(access, parameter.name, parameter.type,
                                          non_access_modifier)) << whitespace_opt_parser

    split_parameter_parser = Parser.sep_by(parameter_parser, string(",").then(whitespace_opt_parser))
    method_parser: Parser = seq(access_parser, non_access_modifier_parser, method_name_parser, string("("),
                                split_parameter_parser, string("): "), type_parser).combine(
        lambda access, non_access_modifier, method_name, open_bracket, parameters, close_bracket,
               type: SemanticModelBuilder.create_method(access, method_name, type, parameters,
                                                        non_access_modifier)) << whitespace_opt_parser

    concept_name_parser: Parser = single_word_pattern.desc('a single word as class name')

    constructor_parser: Parser = seq(access_parser, concept_name_parser, open_bracket_parser, split_parameter_parser,
                                     closing_bracket_parser, string("<<Constructor>>")).combine(
        lambda access, class_name, open_bracket, parameters, closing_bracket, constructor:
        SemanticModelBuilder.create_constructor(access, parameters)) << whitespace_opt_parser

    body_concept_parser: Parser = field_parser | method_parser | constructor_parser

    class_body_parser: Parser = open_curly_braces_parser >> body_concept_parser.many() << closing_curly_braces_parser

    class_parser: Parser = string('class ') >> seq(concept_name_parser, class_body_parser.optional()).combine(
        lambda class_name, class_body: SemanticModelBuilder.create_class(class_name,
                                                                         class_body)) << whitespace_opt_parser

    abstract_class_parser: Parser = string("abstract ") >> class_parser.map(
        lambda clazz: Entity(clazz.name, clazz.fields, clazz.methods, clazz.constructors, True,
                             False)) << whitespace_opt_parser

    enum_value_parser: Parser = single_word_pattern.desc('a single word as enum value')
    enum_values_parser: Parser = open_curly_braces_parser >> Parser.sep_by(enum_value_parser,
                                                                           whitespace_opt_parser) << closing_curly_braces_parser
    enum_parser: Parser = string('enum ') >> seq(concept_name_parser, enum_values_parser.optional()).combine(
        lambda class_name, enum_values: SemanticModelBuilder.create_enum(class_name,
                                                                         enum_values)) << whitespace_opt_parser

    interface_body_concept_parser: Parser = field_parser | method_parser
    interface_body_parser: Parser = open_curly_braces_parser >> interface_body_concept_parser.many() << closing_curly_braces_parser
    interface_parser: Parser = string('interface ') >> seq(concept_name_parser,
                                                           interface_body_parser.optional()).combine(
        lambda interface_name, interface_body: SemanticModelBuilder.create_interface(
            interface_name, interface_body)) << whitespace_opt_parser

    extension: Parser = string('<|--').result(DependencyType.EXTENSION)
    composition: Parser = string('*--').result(DependencyType.COMPOSITION)
    aggregation: Parser = string('o--').result(DependencyType.AGGREGATION)
    dependency_type: Parser = extension | composition | aggregation  # | association
    dependency_name: Parser = single_word_pattern.desc('a single word as a dependency name')

    double_quote_term_parser: Parser = regex('"[^"]+"').desc('term surrounded by double quotes e.g "1"')
    cardinality_parser: Parser = double_quote_term_parser.map(
        lambda cardinality: cardinality[1:-1]) << whitespace_parser
    dependency_from = seq(dependency_name, whitespace_parser, cardinality_parser.optional()).combine(
        lambda name, whitespace, cardinality: SemanticModelBuilder.create_dependency_from(name, cardinality))
    dependency_to = seq(cardinality_parser.optional(), dependency_name).combine(
        lambda cardinality, name: SemanticModelBuilder.create_dependency_from(name, cardinality))

    new_line_parser: Parser = string('\n').desc('new line')
    label_parser: Parser = whitespace_opt_parser.then(string(":")).then(
        whitespace_opt_parser) >> regex(".*")

    dependency_parser: Parser = seq(
        dependency_from, whitespace_opt_parser >> dependency_type << whitespace_opt_parser, dependency_to,
        label_parser.optional()).combine(
        lambda _from, dependency_type, to, label: SemanticModelBuilder.create_dependency(
            _from, to, dependency_type, label)) << whitespace_opt_parser

    concept_parser = class_parser | abstract_class_parser | enum_parser | interface_parser | dependency_parser
    plant_uml_parser: Parser = whitespace_opt_parser.then(string('@startuml')).then(
        whitespace_opt_parser) >> concept_parser.many().map(
        lambda concepts: SemanticModelBuilder.create_plant_uml(concepts)
    ) << whitespace_opt_parser.then(string('@enduml')).then(whitespace_opt_parser)
