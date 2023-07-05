import unittest

from casestudytwo.python.PlantUmlParser import PlantUmlParser
from casestudytwo.python.PythonToPlantUml import PythonToPlantUml
from casestudytwo.python.SemanticModel import Access, Field, Parameter, PlantUml, NonAccessModifier, Method, \
    Constructor, Dependency


class MyTestCase(unittest.TestCase):
    # ''' _________________ Single Parser Tests _________________ '''
    # _________________ Constructor  _________________
    def test_constructor_without_parameters(self):
        # GIVEN
        constructor = "+ ClassName() <<Constructor>>"

        # WHEN
        result: Constructor = PlantUmlParser.constructor_parser.parse(constructor)

        # THEN
        self.assertTrue(result.access == Access.public)
        self.assertFalse(result.parameters)

    def test_constructor_with_parameters(self):
        # GIVEN
        constructor = "+ ClassName(firstParam: String, secondParam: int) <<Constructor>>"

        # WHEN
        result = PlantUmlParser.constructor_parser.parse(constructor)

        # THEN
        self.assertEqual(result.access, Access.public)
        self.assertTrue(len(result.parameters), 2)
        self.assertEqual(result.parameters[0].name, "firstParam")
        self.assertEqual(result.parameters[0].type, "String")
        self.assertEqual(result.parameters[1].name, "secondParam")
        self.assertEqual(result.parameters[1].type, "int")

    # _________________ Parameter  _________________
    def test_parameter_with_parameters(self):
        # GIVEN
        parameter = "firstParam: String"

        # WHEN
        result: Parameter = PlantUmlParser.parameter_parser.parse(parameter)

        # THEN
        self.assertEqual(result.name, "firstParam")
        self.assertEqual(result.type, "String")

    # _________________ Methods  _________________
    def test_method_without_parameter(self):
        # GIVEN
        method = "- testMethod(): Unit"

        # WHEN
        result: Method = PlantUmlParser.method_parser.parse(method)

        # THEN
        self.assertEqual(result.access, Access.private)
        self.assertEqual(result.name, "testMethod")
        self.assertFalse(result.parameters)
        self.assertEqual(result.type, "Unit")
        self.assertIsNone(result.non_access_modifier)

    def test_method_with_parameters(self):
        # GIVEN
        method = "+ testMethod(firstParameter: Double, secondParameter: int): Unit"

        # WHEN
        result: Method = PlantUmlParser.method_parser.parse(method)

        # THEN
        self.assertEqual(result.access, Access.public)
        self.assertEqual(result.name, "testMethod")
        self.assertTrue(len(result.parameters), 2)
        self.assertEqual(result.parameters[0].name, "firstParameter")
        self.assertEqual(result.parameters[0].type, "Double")
        self.assertEqual(result.parameters[1].name, "secondParameter")
        self.assertEqual(result.parameters[1].type, "int")
        self.assertEqual(result.type, "Unit")

    # _________________ Fields  _________________
    def test_field_without_non_access_modifier(self):
        # GIVEN
        field = "# testField: String"

        # WHEN
        result: Field = PlantUmlParser.field_parser.parse(field)

        # THEN
        self.assertEqual(result.access, Access.protected)
        self.assertEqual(result.name, "testField")
        self.assertEqual(result.type, "String")
        self.assertIsNone(result.non_access_modifier)

    def test_field_with_non_access_modifier(self):
        # GIVEN
        field = "# {static} testField: String"

        # WHEN
        result: Field = PlantUmlParser.field_parser.parse(field)

        # THEN
        self.assertEqual(result.access, Access.protected)
        self.assertEqual(result.name, "testField")
        self.assertEqual(result.type, "String")
        self.assertEqual(result.non_access_modifier, NonAccessModifier.STATIC)

    # _________________ static and abstract fields and methods  _________________
    def test_static_and_abstract_fields_and_methods(self):
        # GIVEN
        plant_uml = """
        @startuml
        class MyClass {
        + {static} staticMethod(): void
        + {abstract} abstractMethod(): void
        + {static} staticField: String
        + {abstract} abstractField: String
        }
        @enduml"""

        # WHEN
        result: PlantUml = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN

        self.assertTrue(len(result.classes) == 1)
        self.assertTrue(len(result.classes[0].methods) == 2)
        self.assertEqual(result.classes[0].methods[0].non_access_modifier, NonAccessModifier.STATIC)
        self.assertEqual(result.classes[0].methods[0].name, "staticMethod")
        self.assertEqual(result.classes[0].methods[0].type, "void")
        self.assertEqual(result.classes[0].methods[1].non_access_modifier, NonAccessModifier.ABSTRACT)
        self.assertEqual(result.classes[0].methods[1].name, "abstractMethod")
        self.assertEqual(result.classes[0].methods[1].type, "void")
        self.assertTrue(len(result.classes[0].fields) == 2)
        self.assertEqual(result.classes[0].fields[0].non_access_modifier, NonAccessModifier.STATIC)
        self.assertEqual(result.classes[0].fields[0].name, "staticField")
        self.assertEqual(result.classes[0].fields[0].type, "String")
        self.assertEqual(result.classes[0].fields[1].non_access_modifier, NonAccessModifier.ABSTRACT)
        self.assertEqual(result.classes[0].fields[1].name, "abstractField")
        self.assertEqual(result.classes[0].fields[1].type, "String")

    # _________________ Class _________________
    def test_class_with_fields_methods_and_constructor(self):
        # GIVEN
        plant_uml = """
        @startuml
        class MyClass {
        - privateField: String
        # protectedField: int
        + publicField: double
        ~ packageField: boolean
        + MyClass() <<Constructor>>
        + publicMethod(): void
        # protectedMethod(): int
        - privateMethod(): String
        ~ packageMethod(): boolean
        }
        @enduml"""

        # WHEN
        result = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        self.assertTrue(len(result.classes) == 1)
        self.assertEqual(result.classes[0].name, "MyClass")
        self.assertTrue(len(result.classes[0].fields) == 4)
        self.assertEqual(result.classes[0].fields[0].access, Access.private)
        self.assertEqual(result.classes[0].fields[0].name, "privateField")
        self.assertEqual(result.classes[0].fields[0].type, "String")
        self.assertEqual(result.classes[0].fields[3].access, Access.packagePrivate)
        self.assertEqual(result.classes[0].fields[3].name, "packageField")
        self.assertEqual(result.classes[0].fields[3].type, "boolean")
        self.assertTrue(len(result.classes[0].methods) == 4)
        self.assertEqual(result.classes[0].methods[0].access, Access.public)
        self.assertEqual(result.classes[0].methods[0].name, "publicMethod")
        self.assertFalse(result.classes[0].methods[0].parameters)
        self.assertEqual(result.classes[0].methods[0].type, "void")
        self.assertEqual(result.classes[0].methods[3].access, Access.packagePrivate)
        self.assertEqual(result.classes[0].methods[3].name, "packageMethod")
        self.assertFalse(result.classes[0].methods[3].parameters)
        self.assertEqual(result.classes[0].methods[3].type, "boolean")
        self.assertTrue(len(result.classes[0].constructors) == 1)
        self.assertEqual(result.classes[0].constructors[0].access, Access.public)
        self.assertFalse(result.classes[0].constructors[0].parameters)

    def test_class_without_body(self):
        # GIVEN
        plant_uml = """
        @startuml
        class MyClass
        @enduml"""

        # WHEN
        result: PlantUml = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        self.assertTrue(len(result.classes) == 1)
        self.assertEqual(result.classes[0].name, "MyClass")
        self.assertFalse(result.classes[0].fields)
        self.assertFalse(result.classes[0].methods)
        self.assertFalse(result.classes[0].constructors)
        self.assertFalse(result.classes[0].is_abstract)

    #
    def test_class_body_with_different_order(self):
        # GIVEN
        plant_uml = """
        @startuml
        class MyClass {
        + publicMethod(): void
        - privateField: String
        }
        @enduml"""

        # WHEN
        result = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        self.assertTrue(len(result.classes) == 1)
        self.assertTrue(len(result.classes[0].methods) == 1)
        self.assertTrue(len(result.classes[0].fields) == 1)

        # ________________ Abstract class _________________

    def test_abstract_class_with_fields(self):
        # GIVEN
        plant_uml = """
        @startuml
        abstract class MyClass {
        - privateField: String
        }
        @enduml"""

        # WHEN
        result: PlantUml = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        first_abstract_class = result.abstract_classes[0]
        self.assertTrue(first_abstract_class.is_abstract)
        self.assertTrue(len(result.abstract_classes) == 1)
        self.assertEqual(first_abstract_class.name, "MyClass")
        self.assertTrue(len(first_abstract_class.fields) == 1)
        self.assertEqual(first_abstract_class.fields[0].access, Access.private)
        self.assertEqual(first_abstract_class.fields[0].name, "privateField")
        self.assertEqual(first_abstract_class.fields[0].type, "String")

    def test_abstract_class_without_body(self):
        # GIVEN
        plant_uml = """
        @startuml
        abstract class MyClass
        @enduml"""

        # WHEN
        result = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        self.assertFalse(result.classes)
        self.assertTrue(result.abstract_classes)
        self.assertTrue(len(result.abstract_classes) == 1)
        first_abstract_class = result.abstract_classes[0]
        self.assertEqual(first_abstract_class.name, "MyClass")
        self.assertFalse(first_abstract_class.fields)
        self.assertFalse(first_abstract_class.methods)
        self.assertFalse(first_abstract_class.constructors)
        self.assertTrue(first_abstract_class.is_abstract)

    # _________________ Enum _________________
    def test_enum_with_body(self):
        # GIVEN
        plant_uml = """
        @startuml
        enum TimeUnit {
        DAYS
        HOURS
        MINUTES
        }
        @enduml"""

        # WHEN
        result: PlantUml = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        self.assertTrue(len(result.enums) == 1)
        self.assertEqual(result.enums[0].name, "TimeUnit")
        self.assertTrue(len(result.enums[0].values) == 3)
        self.assertEqual(result.enums[0].values[0], "DAYS")
        self.assertEqual(result.enums[0].values[2], "MINUTES")

    def test_enum_without_body(self):
        # GIVEN
        plant_uml = """
        @startuml
        enum TimeUnit
        @enduml"""

        # WHEN
        result: PlantUml = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        self.assertTrue(result.enums)
        self.assertTrue(len(result.enums) == 1)
        self.assertEqual(result.enums[0].name, "TimeUnit")
        self.assertFalse(result.enums[0].values)

    # _________________ Interface _________________
    def test_interface_with_body(self):
        # GIVEN
        plant_uml = """
        @startuml
        interface InterfaceName {
        - privateField: String
        + publicMethod(): void
        }
        interface InterfaceName2 {
        - privateField2: String
        + publicMethod2(): void
        }
        @enduml"""

        # WHEN
        result: PlantUml = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        second_interface = result.interfaces[1]
        first_interface = result.interfaces[0]

        self.assertTrue(len(result.interfaces) == 2)
        self.assertTrue(first_interface.is_interface)
        self.assertFalse(first_interface.is_abstract)
        self.assertEqual(first_interface.name, "InterfaceName")
        self.assertTrue(len(first_interface.fields) == 1)
        self.assertEqual(first_interface.fields[0].access, Access.private)
        self.assertEqual(first_interface.fields[0].name, "privateField")
        self.assertEqual(first_interface.fields[0].type, "String")
        self.assertTrue(len(first_interface.methods) == 1)
        self.assertEqual(first_interface.methods[0].access, Access.public)
        self.assertEqual(first_interface.methods[0].name, "publicMethod")
        self.assertEqual(first_interface.methods[0].type, "void")
        self.assertFalse(first_interface.constructors)
        self.assertTrue(second_interface.is_interface)
        self.assertFalse(second_interface.is_abstract)
        self.assertEqual(second_interface.name, "InterfaceName2")
        self.assertTrue(len(second_interface.fields) == 1)
        self.assertEqual(second_interface.fields[0].access, Access.private)
        self.assertEqual(second_interface.fields[0].name, "privateField2")
        self.assertEqual(second_interface.fields[0].type, "String")
        self.assertTrue(len(second_interface.methods) == 1)
        self.assertEqual(second_interface.methods[0].access, Access.public)
        self.assertEqual(second_interface.methods[0].name, "publicMethod2")
        self.assertEqual(second_interface.methods[0].type, "void")
        self.assertFalse(second_interface.constructors)

    def test_interface_without_body(self):
        # GIVEN
        plant_uml = """
        @startuml
        interface InterfaceName
        interface InterfaceName2
        @enduml"""

        # WHEN
        result: PlantUml = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        first_interface = result.interfaces[0]
        second_interface = result.interfaces[1]

        self.assertTrue(first_interface.is_interface)
        self.assertFalse(first_interface.is_abstract)
        self.assertEqual(first_interface.name, "InterfaceName")
        self.assertFalse(first_interface.fields)
        self.assertFalse(first_interface.methods)

        self.assertTrue(second_interface.is_interface)
        self.assertFalse(second_interface.is_abstract)
        self.assertTrue(len(result.interfaces) == 2)
        self.assertEqual(second_interface.name, "InterfaceName2")
        self.assertFalse(second_interface.fields)
        self.assertFalse(second_interface.methods)

        # _________________ Dependency _________________

    def test_dependency_between_concepts(self):
        # GIVEN
        plant_uml = """
        @startuml
        class Class
        class Class2
        enum Enum
        abstract class AbstractClass
        interface Interface
        AbstractClass <|-- Class
        Class <|-- Class2
        Class2 *-- Enum
        Class2 *-- Interface
        @enduml"""

        # WHEN
        result_object: PlantUml = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        self.assertTrue(len(result_object.abstract_classes) == 1)
        self.assertEqual(result_object.abstract_classes[0].name, "AbstractClass")
        self.assertTrue(result_object.abstract_classes[0].is_abstract)
        self.assertTrue(len(result_object.classes) == 2)
        self.assertEqual(result_object.classes[0].name, "Class")
        self.assertEqual(result_object.classes[1].name, "Class2")
        self.assertTrue(len(result_object.enums) == 1)
        self.assertEqual(result_object.enums[0].name, "Enum")
        self.assertTrue(len(result_object.interfaces) == 1)
        self.assertEqual(result_object.interfaces[0].name, "Interface")
        self.assertTrue(len(result_object.dependencies) == 4)
        self.assertEqual(result_object.dependencies[0].from_.name, "AbstractClass")
        self.assertEqual(result_object.dependencies[0].to.name, "Class")
        third_dependency = result_object.dependencies[1]
        self.assertEqual(third_dependency.from_.name, "Class")
        self.assertEqual(third_dependency.to.name, "Class2")

    # _________________ Dependency _________________

    def test_dependency_between_concepts_with_cardinality(self):
        # GIVEN
        plant_uml = """
        @startuml
        class Class
        class Class2
        enum Enum
        
        Class "1" <|-- "many" Class2
        Class2 *-- Enum
        @enduml"""

        # WHEN
        result_object: PlantUml = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        first_dependency = result_object.dependencies[0]
        self.assertEqual(first_dependency.from_.name, "Class")
        self.assertEqual(first_dependency.to.name, "Class2")
        self.assertEqual(first_dependency.from_.cardinality, "1")
        self.assertEqual(first_dependency.to.cardinality, "many")

        second_dependency = result_object.dependencies[1]
        self.assertEqual(second_dependency.from_.name, "Class2")
        self.assertEqual(second_dependency.to.name, "Enum")
        self.assertEqual(second_dependency.from_.cardinality, None)
        self.assertEqual(second_dependency.to.cardinality, None)

    def test_dependency_between_concepts_with_label(self):
        # GIVEN
        plant_uml = """
        @startuml
        class Class
        class Class2
        abstract class AbstractClass
        AbstractClass <|-- Class : label test
        Class "1" <|-- "many" Class2 : test
        @enduml"""

        # WHEN
        result_object: PlantUml = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        first_dependency: Dependency = result_object.dependencies[0]
        self.assertEqual(first_dependency.from_.name, "AbstractClass")
        self.assertEqual(first_dependency.to.name, "Class")
        self.assertEqual(first_dependency.label, "label test")

        second_dependency: Dependency = result_object.dependencies[1]
        self.assertEqual(second_dependency.from_.name, "Class")
        self.assertEqual(second_dependency.to.name, "Class2")
        self.assertEqual(second_dependency.from_.cardinality, "1")
        self.assertEqual(second_dependency.to.cardinality, "many")
        self.assertEqual(second_dependency.label, "test")

        # _________________ With all concepts _________________

    def test_with_all_concepts_multiple_times_without_body(self):
        # GIVEN
        plant_uml = """
        @startuml
        class Class
        class Class2
        enum Enum
        abstract class AbstractClass
        interface Interface
        abstract class AbstractClass2
        enum Enum2
        interface Interface2
        @enduml
        """

        # WHEN
        result = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        self.assertTrue(len(result.abstract_classes) == 2)
        self.assertEqual(result.abstract_classes[0].name, "AbstractClass")
        self.assertTrue(result.abstract_classes[0].is_abstract)
        self.assertEqual(result.abstract_classes[1].name, "AbstractClass2")
        self.assertTrue(result.abstract_classes[1].is_abstract)
        self.assertTrue(len(result.classes) == 2)
        self.assertEqual(result.classes[0].name, "Class")
        self.assertFalse(result.classes[0].is_abstract)
        self.assertEqual(result.classes[1].name, "Class2")
        self.assertFalse(result.classes[1].is_abstract)
        self.assertTrue(len(result.enums) == 2)
        self.assertEqual(result.enums[0].name, "Enum")
        self.assertEqual(result.enums[1].name, "Enum2")
        self.assertTrue(len(result.interfaces) == 2)
        self.assertEqual(result.interfaces[0].name, "Interface")
        self.assertFalse(result.interfaces[0].is_abstract)
        self.assertEqual(result.interfaces[1].name, "Interface2")
        self.assertFalse(result.interfaces[1].is_abstract)

    def test_with_all_concepts_multiple_times_with_body(self):
        # GIVEN
        plant_uml = """
        @startuml
        class Class {
        - privateField: String
        + Class() <<Constructor>>
        - privateMethod(): String
        }
        enum Enum {
        DAYS
        HOURS
        MINUTES
        }
        abstract class AbstractClass {
        - privateField: String
        + AbstractClass() <<Constructor>>
        - privateMethod(): String
        }
        interface InterfaceName {
        - privateField: String
        + publicMethod(): void
        }

        AbstractClass <|-- Class
        Class <|-- Class2
        Class2 *-- Enum
        Class2 *-- InterfaceName
        @enduml"""

        # WHEN
        result_object: PlantUml = PlantUmlParser.plant_uml_parser.parse(plant_uml)

        # THEN
        self.assertTrue(len(result_object.abstract_classes) == 1)
        self.assertEqual(result_object.abstract_classes[0].name, "AbstractClass")
        self.assertTrue(result_object.abstract_classes[0].is_abstract)
        self.assertTrue(len(result_object.classes) == 1)
        self.assertEqual(result_object.classes[0].name, "Class")
        self.assertFalse(result_object.classes[0].is_abstract)
        self.assertTrue(len(result_object.enums) == 1)
        self.assertEqual(result_object.enums[0].name, "Enum")
        self.assertTrue(len(result_object.interfaces) == 1)
        self.assertEqual(result_object.interfaces[0].name, "InterfaceName")

        self.assertTrue(len(result_object.abstract_classes[0].fields) == 1)
        self.assertEqual(result_object.abstract_classes[0].fields[0].access, Access.private)
        self.assertEqual(result_object.abstract_classes[0].fields[0].name, "privateField")
        self.assertEqual(result_object.abstract_classes[0].fields[0].type, "String")
        self.assertTrue(len(result_object.abstract_classes[0].constructors) == 1)
        self.assertEqual(result_object.abstract_classes[0].constructors[0].access, Access.public)
        self.assertFalse(result_object.abstract_classes[0].constructors[0].parameters)
        self.assertTrue(len(result_object.abstract_classes[0].methods) == 1)
        self.assertEqual(result_object.abstract_classes[0].methods[0].access, Access.private)
        self.assertEqual(result_object.abstract_classes[0].methods[0].name, "privateMethod")
        self.assertEqual(result_object.abstract_classes[0].methods[0].type, "String")
        self.assertFalse(result_object.abstract_classes[0].methods[0].parameters)

        self.assertTrue(len(result_object.classes[0].fields) == 1)
        self.assertEqual(result_object.classes[0].fields[0].access, Access.private)
        self.assertEqual(result_object.classes[0].fields[0].name, "privateField")
        self.assertEqual(result_object.classes[0].fields[0].type, "String")
        self.assertTrue(len(result_object.classes[0].constructors) == 1)
        self.assertEqual(result_object.classes[0].constructors[0].access, Access.public)
        self.assertFalse(result_object.classes[0].constructors[0].parameters)
        self.assertTrue(len(result_object.classes[0].methods) == 1)
        self.assertEqual(result_object.classes[0].methods[0].access, Access.private)
        self.assertEqual(result_object.classes[0].methods[0].name, "privateMethod")
        self.assertEqual(result_object.classes[0].methods[0].type, "String")
        self.assertFalse(result_object.classes[0].methods[0].parameters)

        self.assertTrue(len(result_object.enums[0].values) == 3)
        self.assertEqual(result_object.enums[0].values[0], "DAYS")
        self.assertEqual(result_object.enums[0].values[2], "MINUTES")

        self.assertTrue(len(result_object.interfaces[0].fields) == 1)
        self.assertEqual(result_object.interfaces[0].fields[0].access, Access.private)
        self.assertEqual(result_object.interfaces[0].fields[0].name, "privateField")
        self.assertEqual(result_object.interfaces[0].fields[0].type, "String")
        self.assertTrue(len(result_object.interfaces[0].methods) == 1)
        self.assertEqual(result_object.interfaces[0].methods[0].access, Access.public)
        self.assertEqual(result_object.interfaces[0].methods[0].name, "publicMethod")
        self.assertEqual(result_object.interfaces[0].methods[0].type, "void")
        self.assertFalse(result_object.interfaces[0].methods[0].parameters)

    def test_for_loc(self):
        # GIVEN
        plant_uml = """
        @startuml
class ClassName {
- {static} privateField: String
+ ClassName(privateField: String) <<Constructor>>
+ {static} publicMethod(parameter: String): void
}
abstract class AbstractClassName {
# {abstract} protectedField: int
+ AbstractClassName(protectedField: int) <<Constructor>>
- {static} privateMethod(parameter: String): void
}
enum EnumName {
VALUE1
VALUE2
VALUE3
}
interface InterfaceName {
+ publicField: String
+ publicMethod(parameter: String): Map
}
ClassName <|-- EnumName
ClassName "1" *-- "many" AbstractClassName : test label
AbstractClassName o-- "*" ClassName
ClassName o-- AbstractClassName : test
@enduml"""

        # WHEN
        result_object: PlantUml = PlantUmlParser.plant_uml_parser.parse(plant_uml)
        result_string = PythonToPlantUml.map_plant_uml_to_plant_uml_string(result_object)

        # THEN
        self.assertEqual(result_string.strip(), plant_uml.strip())


if __name__ == '__main__':
    unittest.main()
