from KnowledgeExtractionEngine.TextExtractor.patterns_matcher.pattern import Pattern


class RelationPatternBuilder:
    def __init__(self, **patterns):
        """
        Initialize the patterns
        """

        self.ABSTRACT_PATTERN = Pattern("ABSTRACT", [
            [{"LEMMA": "be"}, {"LOWER": "abstract"}],
            [{"LOWER": "abstract"}, {"LOWER": "class"}, {"POS": "NOUN"}],
            [{"LOWER": "abstract"}, {"LOWER": "class"}, {"POS": "PROPN"}]
        ])

        self.HAS_METHOD_PATTERN = Pattern("HAS_METHOD", [
            [{"LEMMA": "have"}, {"POS": "DET"}, {"LEMMA": "method"}],
            [{"LEMMA": "call"}]])

        self.HAS_PARENT_PATTERN = Pattern("HAS_PARENT", [
            [{"TEXT": "in"}]])

        self.BE_METHOD_PATTERN = Pattern("BE_METHOD", [
            [{"LEMMA": "be"}, {"POS": "DET", "OP": "*"}, {"LEMMA": "method"}],
        ])

        self.HAS_ATTRIBUTE_PATTERN = Pattern("HAS_ATTRIBUTE", [
            [{"LEMMA": "have"}, {"POS": "DET", "OP": "*"}, {"LEMMA": "attribute"}],
            [{"LEMMA": "be"}, {"POS": "DET", "OP": "*"}, {"LEMMA": "attribute"}],
        ])

        self.BE_SUBCLASS_PATTERN = Pattern("SUBCLASS", [
            [{"LEMMA": "inherit"}, {"ADP": "from", "OP": "?"}],
            [{"LEMMA": "be"}, {"LOWER": "subclass"}, {"ADP": "of"}],
        ])

        self.BE_SUPERCLASS_PATTERN = Pattern("SUPERCLASS", [
            [{"LEMMA": "be"}, {"LOWER": "superclass"}, {"ADP": "of"}],
            [{"LEMMA": "can"}, {"LEMMA": "be"}]
        ])

        self.REALIZATION_PATTERN = Pattern("REALIZATION", [
            [{"LEMMA": "implement"}],
            [{"LEMMA": "realize"}],
            [{"LEMMA": "realise"}],
            [{"LEMMA": "be"}, {"LOWER": "realisation"}, {"ADP": "of", "OP": "?"}],
            [{"LEMMA": "be"}, {"LOWER": "realization"}, {"ADP": "of", "OP": "?"}]
        ])

        self.UNIDIRECTIONAL_ASSOCIATION_PATTERN = Pattern("UNIDIRECTIONAL", [
            [{"LEMMA": "use"}],
            [{"LEMMA": "invoke"}]
        ])
        self.DEPENDENCY_ASSOCIATION_PATTERN = Pattern("DEPENDENCY", [
            [{"LEMMA": "call"}],
        ])

        self.BIDIRECTIONAL_ASSOCIATION_PATTERN = Pattern("BIDIRECTIONAL", [])

        self.COMPOSITION_PATTERN_1 = Pattern("COMPOSITION1", [
            [{"LEMMA": "be"}, {"LOWER": "composed"}, {"ADP": "of", "OP": "?"}],
            [{"LEMMA": "contain"}]
        ])

        self.COMPOSITION_PATTERN_2 = Pattern("COMPOSITION2", [
            [{"LEMMA": "be"}, {"LOWER": "part"}, {"ADP": "of", "OP": "?"}]
        ])

        self.RELATION_PATTERNS = [self.ABSTRACT_PATTERN, self.BE_SUBCLASS_PATTERN, self.BE_SUPERCLASS_PATTERN,
                                  self.REALIZATION_PATTERN, self.DEPENDENCY_ASSOCIATION_PATTERN,
                                  self.HAS_ATTRIBUTE_PATTERN, self.HAS_METHOD_PATTERN, self.BE_METHOD_PATTERN,
                                  self.UNIDIRECTIONAL_ASSOCIATION_PATTERN, self.BIDIRECTIONAL_ASSOCIATION_PATTERN,
                                  self.COMPOSITION_PATTERN_1, self.COMPOSITION_PATTERN_2, self.HAS_PARENT_PATTERN]
        # Vector enumerating possible associations between UML classes
    #   self.UML_ASSOCIATIONS = ["be subclass of", "be superclass of", "implement","be implemented by", "be composed of", "be part of", "has parent"]
