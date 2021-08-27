class TemplateBuilder:
    def __init__(self, **templates):
        """
        Initialize the templates
        """

        self.BE_CLASS_TEMPLATE = [{"CLASS": ""}, {"BE_CLASS": "is class"}]

        self.BE_INTERFACE_TEMPLATE = [{"INTERFACE": ""}, {"BE_INTERFACE": "is interface"}]

        self.BE_ENUM_TEMPLATE = [{"ENUM": ""}, {"BE_ENUM": "is enum"}]

        self.BE_ATTRIBUTE_TEMPLATE = [{"ATTRIBUTE": ""}, {"BE_ATTRIBUTE": "is attribute"}]

        self.BE_METHOD_TEMPLATE = [{"METHOD": ""}, {"BE_METHOD": "is method"}]

        self.ABSTRACT_TEMPLATE = [[{"CLASS": ""}, {"ABSTRACT": "is abstract"}]]

        self.HAS_METHOD_TEMPLATE = [[{"CLASS": ""},{ "HAS_METHOD": "has method"}, {"METHOD": ""}],
                                    [{"INTERFACE": ""},{ "HAS_METHOD": "has method"}, {"METHOD": ""}]]

        self.BE_SUBCLASS_TEMPLATE = [[{"CLASS": ""}, {"SUBCLASS": "is subclass of"}, {"CLASS": ""}]]

        self.BE_SUPERCLASS_TEMPLATE = [[{"CLASS": ""}, {"SUPERCLASS#": "is superclass of"}, {"CLASS": ""}]]

        self.REALIZATION_TEMPLATE = [[{"CLASS": ""}, {"REALIZATION": "implements"}, {"INTERFACE": ""}]]

        self.COMPOSITION1_TEMPLATE = [[{"CLASS": ""}, {"COMPOSITION1": "is composed of"},{ "CLASS": ""}]]

        self.COMPOSITION2_TEMPLATE = [[{"CLASS": ""}, {"COMPOSITION2": "is part of"}, {"CLASS": ""}]]

        self.UNIDIRECTIONAL_TEMPLATE = [[{"CLASS": ""}, {"UNIDIRECTIONAL": "uses"}, {"CLASS": ""}],
                                        [{"INTERFACE": ""}, {"UNIDIRECTIONAL": "uses"}, {"CLASS": ""}],
                                        [{"CLASS": ""}, {"UNIDIRECTIONAL": "uses"}, {"INTERFACE": ""}]]
        self.DEPENDENCY_TEMPLATE = [[{"CLASS": ""}, {"DEPENDENCY": "calls"}, {"CLASS": ""}]]

        self.ALL_RELATIONS_TEMPLATES = [self.ABSTRACT_TEMPLATE, self.HAS_METHOD_TEMPLATE, self.BE_SUBCLASS_TEMPLATE,
                                        self.BE_SUPERCLASS_TEMPLATE, self.REALIZATION_TEMPLATE,
                                        self.COMPOSITION1_TEMPLATE, self.COMPOSITION2_TEMPLATE,
                                        self.UNIDIRECTIONAL_TEMPLATE, self.DEPENDENCY_TEMPLATE]

        self.ALL_TYPES_TEMPLATES = [self.BE_CLASS_TEMPLATE, self.BE_ENUM_TEMPLATE, self.BE_INTERFACE_TEMPLATE,
                                    self.BE_METHOD_TEMPLATE, self.BE_ATTRIBUTE_TEMPLATE]

        self.ALL_ASSOCIATIONS = ["ABSTRACT", "HAS_METHOD", "SUBCLASS", "SUPERCLASS", "REALIZATION"]

        # Vector enumerating possible properties of a UML class
        self.CLASS_PROPERTIES = ["is abstract", "has method", "has attribute"]

        # Vector enumerating possible associations between UML classes
        self.UML_ASSOCIATIONS = ["is subclass of", "is superclass of", "implements", "uses", "calls",
                                 "is composed of", "is part of"]
