from enum import Enum

from typing import List


class Access(Enum):
    public = 1
    private = 2
    protected = 3
    packagePrivate = 4


class NonAccessModifier(Enum):
    ABSTRACT = 1
    STATIC = 2


class DependencyType(Enum):
    EXTENSION = 1
    COMPOSITION = 2
    AGGREGATION = 3


class Field:
    def __init__(self, access: Access, name: str, type: str, non_access_modifier: NonAccessModifier):
        self.access = access
        self.name = name
        self.type = type
        self.non_access_modifier = non_access_modifier

class Parameter:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type


class Method:
    def __init__(self, access: Access, name: str, type: str, parameters: List[Parameter],
                 non_access_modifier: NonAccessModifier):
        self.access = access
        self.name = name
        self.type = type
        self.parameters = parameters
        self.non_access_modifier = non_access_modifier


class Constructor:
    def __init__(self, access: Access, parameters: List[Parameter]):
        self.access = access
        self.parameters = parameters


class Entity:
    def __init__(self, name: str, fields: List[Field], methods: List[Method], constructors: List[Constructor],
                 is_abstract: bool, is_interface: bool):
        self.name = name
        self.fields = fields
        self.methods = methods
        self.constructors = constructors
        self.is_abstract = is_abstract
        self.is_interface = is_interface


class Enumeration:
    def __init__(self, name: str, values: List[str]):
        self.name = name
        self.values = values


class DependencyConcept:
    def __init__(self, name: str, cardinality: str):
        self.name = name
        self.cardinality = cardinality


class Dependency:
    def __init__(self, from_: DependencyConcept, to: DependencyConcept, dependency_type: DependencyType, label: str):
        self.from_ = from_
        self.to = to
        self.dependency_type = dependency_type
        self.label = label


class PlantUml:
    def __init__(self, classes: List[Entity], abstract_classes: List[Entity], enums: List[Enumeration],
                 interfaces: List[Entity], dependencies: List[Dependency]):
        self.classes = classes
        self.abstract_classes = abstract_classes
        self.enums = enums
        self.interfaces = interfaces
        self.dependencies = dependencies
