from typing import List, Tuple

from casestudytwo.python.SemanticModel import NonAccessModifier, Access, Entity, PlantUml, Parameter, Field, Method, \
    Constructor, Dependency, Enumeration, DependencyType, DependencyConcept


class SemanticModelBuilder:
    @staticmethod
    def create_class(name: str, body):
        body_concepts: Tuple[List[Field], List[Method], List[Constructor]] = SemanticModelBuilder.map_body_to_type(
            body) if body is not None else ([], [], [])
        return Entity(name, body_concepts[0], body_concepts[1], body_concepts[2], False, False)

    @staticmethod
    def create_plant_uml(concepts):
        class_concepts: Tuple[
            List[Entity], List[Entity], List[Enumeration], List[Entity], List[
                Dependency]] = SemanticModelBuilder.map_concept_to_type(
            concepts) if concepts is not None else ([], [], [], [], [])
        return PlantUml(class_concepts[0], class_concepts[1], class_concepts[2], class_concepts[3],
                        class_concepts[4])

    @staticmethod
    def create_parameter(name: str, type: str):
        return Parameter(name, type)

    @staticmethod
    def create_field(access: Access, name: str, type: str, non_access_modifier: NonAccessModifier):
        return Field(access, name, type, non_access_modifier)

    @staticmethod
    def create_method(access, method_name, type, parameters, non_access_modifier):
        return Method(access, method_name, type, parameters, non_access_modifier)

    @staticmethod
    def create_constructor(access, parameters):
        return Constructor(access, parameters)

    @staticmethod
    def map_body_to_type(body: List) -> Tuple[List[Field], List[Method], List[Constructor]]:
        fields: list[Field] = []
        methods: list[Method] = []
        constructors: list[Constructor] = []

        for obj in body:
            if isinstance(obj, Field):
                fields.append(obj)
            elif isinstance(obj, Method):
                methods.append(obj)
            elif isinstance(obj, Constructor):
                constructors.append(obj)
        return fields, methods, constructors

    @staticmethod
    def map_concept_to_type(concepts: List) -> Tuple[
        List[Entity], List[Entity], List[Enumeration], List[Entity], List[Dependency]]:

        classes: list[Entity] = []
        abstract_classes: list[Entity] = []
        interfaces: list[Entity] = []
        enums: list[Enumeration] = []
        dependencies: list[Dependency] = []

        for obj in concepts:
            if isinstance(obj, Entity) and obj.is_interface:
                interfaces.append(obj)
            elif isinstance(obj, Entity) and obj.is_abstract:
                abstract_classes.append(obj)
            elif isinstance(obj, Entity):
                classes.append(obj)
            elif isinstance(obj, Enumeration):
                enums.append(obj)
            elif isinstance(obj, Dependency):
                dependencies.append(obj)
        return classes, abstract_classes, enums, interfaces, dependencies

    @staticmethod
    def create_enum(class_name, enum_values):
        return Enumeration(class_name, enum_values)

    @staticmethod
    def create_interface(class_name, interface_body):
        body_concepts: Tuple[List[Field], List[Method], List[Constructor]] = SemanticModelBuilder.map_body_to_type(
            interface_body) if interface_body is not None else ([], [], [])
        return Entity(class_name, body_concepts[0], body_concepts[1], body_concepts[2], False, True)

    @staticmethod
    def create_dependency(_from: DependencyConcept, to: DependencyConcept,
                          dependency_type: DependencyType, label: str) -> Dependency:
        return Dependency(_from, to, dependency_type, label)

    @staticmethod
    def create_dependency_from(name, cardinality) -> DependencyConcept:
        return DependencyConcept(name, cardinality)
