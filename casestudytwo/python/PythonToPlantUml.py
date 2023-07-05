from typing import List, Dict

from casestudytwo.python.SemanticModel import Access, NonAccessModifier, DependencyType, PlantUml, Entity, Enumeration, \
    Method, Field, Parameter, Constructor, Dependency


class PythonToPlantUml:
    access_modifier: Dict[Access, str] = {
        Access.public: '+',
        Access.private: '-',
        Access.protected: '#',
        Access.packagePrivate: '~'
    }

    non_access_modifier: Dict[NonAccessModifier, str] = {
        NonAccessModifier.STATIC: ' {static}',
        NonAccessModifier.ABSTRACT: ' {abstract}',
    }

    dependency_types: Dict[DependencyType, str] = {
        DependencyType.AGGREGATION: 'o--',
        DependencyType.COMPOSITION: '*--',
        DependencyType.EXTENSION: '<|--',
    }

    @staticmethod
    def map_plant_uml_to_plant_uml_string(plant_uml: PlantUml) -> str:
        return (
                "@startuml\n"
                + PythonToPlantUml.map_class_to_class_string(plant_uml.classes)
                + PythonToPlantUml.map_abstract_class_to_abstract_class_string(plant_uml.abstract_classes)
                + PythonToPlantUml.map_enum_to_enum_string(plant_uml.enums)
                + PythonToPlantUml.map_interface_to_interface_string(plant_uml.interfaces)
                + PythonToPlantUml.map_dependencies_to_dependency_string(plant_uml.dependencies)
                + "\n@enduml"
        ).strip()

    @staticmethod
    def map_class_to_class_string(classes: List[Entity]) -> str:
        result = []
        for clazz in classes:
            builder = []
            if not (clazz.methods or clazz.fields or clazz.constructors):
                builder.append(f"class {clazz.name}")
            else:
                builder.append(f"class {clazz.name} {{")
                builder.append(PythonToPlantUml.map_fields_to_field_string(clazz.fields))
                builder.append(PythonToPlantUml.map_constructors_to_constructor_string(clazz.constructors, clazz.name))
                builder.append(PythonToPlantUml.map_methods_to_method_string(clazz.methods))
                builder.append("}")
            result.append("\n".join(builder))
        return "\n".join(result) + "\n"

    @staticmethod
    def map_interface_to_interface_string(interfaces: List[Entity]) -> str:
        result = []
        for interface in interfaces:
            builder = []
            if not (interface.methods or interface.fields):
                builder.append(f"interface {interface.name}")
            else:
                builder.append(f"interface {interface.name} {{")
                builder.append(PythonToPlantUml.map_fields_to_field_string(interface.fields))
                builder.append(PythonToPlantUml.map_methods_to_method_string(interface.methods))
                builder.append("}")
            result.append("\n".join(builder))
        return "\n".join(result) + "\n"

    @staticmethod
    def map_enum_to_enum_string(enums: List[Enumeration]) -> str:
        result = []
        for enumeration in enums:
            builder = []
            if not enumeration.values:
                builder.append(f"enum {enumeration.name}")
            else:
                builder.append(f"enum {enumeration.name} {{")
                builder.append("\n".join(enumeration.values))
                builder.append("}")
            result.append("\n".join(builder))
        return "\n".join(result) + "\n"

    @staticmethod
    def map_abstract_class_to_abstract_class_string(abstract_classes: List[Entity]) -> str:
        result = []
        for abstract_class in abstract_classes:
            builder = []
            if not (abstract_class.methods or abstract_class.fields or abstract_class.constructors):
                builder.append(f"abstract class {abstract_class.name}")
            else:
                builder.append(f"abstract class {abstract_class.name} {{")
                builder.append(PythonToPlantUml.map_fields_to_field_string(abstract_class.fields))
                builder.append(PythonToPlantUml.map_constructors_to_constructor_string(abstract_class.constructors,
                                                                                       abstract_class.name))
                builder.append(PythonToPlantUml.map_methods_to_method_string(abstract_class.methods))
                builder.append("}")
            result.append("\n".join(builder))
        return "\n".join(result) + "\n"

    @staticmethod
    def map_fields_to_field_string(fields: List[Field]) -> str:
        return "\n".join(
            f"{PythonToPlantUml.access_modifier.get(field.access, '')}"
            f"{PythonToPlantUml.non_access_modifier.get(field.non_access_modifier, '')} {field.name}: {field.type}"
            for field in fields
        )

    @staticmethod
    def map_methods_to_method_string(methods: List[Method]) -> str:
        return "\n".join(
            f"{PythonToPlantUml.access_modifier.get(method.access, '')}"
            f"{PythonToPlantUml.non_access_modifier.get(method.non_access_modifier, '')} {method.name}({PythonToPlantUml.map_parameters_to_parameter_string(method.parameters)}): {method.type}"
            for method in methods
        )

    @staticmethod
    def map_parameters_to_parameter_string(parameters: List[Parameter]) -> str:
        return ", ".join(f"{parameter.name}: {parameter.type}" for parameter in parameters)

    @staticmethod
    def map_constructors_to_constructor_string(constructors: List[Constructor], class_name: str) -> str:
        return "\n".join(
            f"{PythonToPlantUml.access_modifier.get(constructor.access, '')} {class_name}({PythonToPlantUml.map_parameters_to_parameter_string(constructor.parameters)}) <<Constructor>>"
            for constructor in constructors
        )

    @staticmethod
    def get_cardinality(string: str) -> str:
        return f" \"{string}\" " if string else " "

    @staticmethod
    def get_label(string: str) -> str:
        return f" : {string}" if string else ""

    @staticmethod
    def map_dependencies_to_dependency_string(dependencies: List[Dependency]) -> str:
        return "\n".join(
            f"{dependency.from_.name}{PythonToPlantUml.get_cardinality(dependency.from_.cardinality)}{PythonToPlantUml.dependency_types[dependency.dependency_type]}{PythonToPlantUml.get_cardinality(dependency.to.cardinality)}{dependency.to.name}{PythonToPlantUml.get_label(dependency.label)}"
            for dependency in dependencies
        )
