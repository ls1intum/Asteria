class SimilarityOptions:
    def __init__(self, **options):
        """
        Initialize the options
        """
        # Weight of the class type when calculating the similarity of two UML classes
        self.CLASS_TYPE_WEIGHT = 0.3

        # Weight of the class name when calculating the similarity of two UML classes
        self.CLASS_NAME_WEIGHT = 0.7

        # Weight of the number of methods when calculating the similarity of two UML classes
        self.METHODS_NUMBER_WEIGHT = 0.1

        # Weight of the number of names when calculating the similarity of two UML classes
        self.METHOD_NAME_WEIGHT = 0.4

        # Weight of the class containing the method when calculating the similarity of two methods
        self.METHOD_PARENT_WEIGHT = 0.35

        # Weight of the number of attributes when calculating the similarity of two UML classes
        self.ATTRIBUTES_NUMBER_WEIGHT = 0.2

        # Weight of the name similarity of their attributes when calculating the similarity of two UML classes
        self.ATTRIBUTE_NAME_WEIGHT = 0.4

        # Weight of the type similarity of their attributes when calculating the similarity of two UML classes
        self.ATTRIBUTE_TYPE_WEIGHT = 0.3

        # Weight of the class containing the method when calculating the similarity of two methods
        self.ATTRIBUTE_PARENT_WEIGHT = 0.35

        # Weight of the relationship type when calculating the similarity of two UML relationships
        self.RELATION_TYPE_WEIGHT = 0.3

        # Weight of the source and destination elements when calculating the similarity of two UML relationships (
        # e.g. in class diagrams)
        self.RELATION_ELEMENT_WEIGHT = 0.25

        # Weight of the source and destination elements when calculating the similarity of two UML component
        # relationships
        self.COMPONENT_RELATION_ELEMENT_WEIGHT = 0.35

        # Weight of the multiplicity when calculating the similarity of two UML relationships
        self.RELATION_MULTIPLICITY_WEIGHT = 0.05

        # Weight of the roles when calculating the similarity of two UML relationships
        self.RELATION_ROLE_WEIGHT = 0.05

        # Vector enumerating different types of UML elements
        self.UML_ELEMENTS_TYPES = ["is class", "is interface", "is enum", "is method", "is attribute"]

        # Vector enumerating possible properties of a UML class
        self.CLASS_PROPERTIES = ["is abstract", "has method", "has attribute"]

        # Vector enumerating possible associations between UML classes
        self.UML_ASSOCIATIONS = ["is implemented by", "implements", "is composed of", "is part of", "has parent",
                                 "calls", "uses", "is called by", "is used by"]

        # Vector enumerating different types of relations of UML elements
        self.RELATIONS = self.UML_ELEMENTS_TYPES + self.CLASS_PROPERTIES + self.UML_ASSOCIATIONS
