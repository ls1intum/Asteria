import enum


class Association(enum.Enum):
    ClassBidirectional = ""
    ClassRealization
    ClassComposition
    ClassInheritance
    ClassDependency
    ClassUnidirectional
    ClassAggregation