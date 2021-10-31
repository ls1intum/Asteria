from KnowledgeExtractionEngine.TextExtractor.patterns_matcher.pattern import Pattern


class EntityPatternsBuilder:
    def __init__(self, **patterns):
        """
        Initialize the patterns
        """
        self.CLASS_PATTERN = Pattern("CLASS", [
            [{"LOWER": "class"}, {"POS": "PROPN"}],
            [{"LOWER": "class"}, {"POS": "NOUN"}],
            [{"POS": "PROPN"}, {"LOWER": "class"}],
            [{"POS": "NOUN"}, {"LOWER": "class"}],
        ])

        self.INTERFACE_PATTERN = Pattern("INTERFACE", [
            [{"LOWER": "interface"}, {"POS": "PROPN"}],
            [{"LOWER": "interface"}, {"POS": "NOUN"}],
            [{"POS": "PROPN"}, {"LOWER": "interface"}],
            [{"POS": "NOUN"}, {"LOWER": "interface"}]])

        self.ENUM_PATTERN = Pattern("ENUM", [
            [{"LOWER": "enum"}, {"POS": "PROPN"}],
            [{"LOWER": "enum"}, {"POS": "NOUN"}],
            [{"POS": "PROPN"}, {"LOWER": "enum"}],
            [{"POS": "NOUN"}, {"LOWER": "enum"}]])

        self.METHOD_PATTERN = Pattern("METHOD", [
            [{"POS": "PROPN"}, {"TEXT": "("}, {"TEXT": ")"}],
            [{"POS": "NOUN"}, {"TEXT": "("}, {"TEXT": ")"}],
            [{"POS": "PROPN"}, {"TEXT": "("}, {"TEXT": ")"}],
            [{"POS": "NOUN"}, {"TEXT": "("}, {"TEXT": ")"}],
            [{"POS": "VERB"}, {"TEXT": "("}, {"TEXT": ")"}]

        ])

        self.ATTRIBUTE_PATTERN = Pattern("ATTRIBUTE", [
            [{"LOWER": "attribute"}, {"POS": "PROPN"}],
            [{"LOWER": "attribute"}, {"POS": "NOUN"}],
            [{"POS": "PROPN"}, {"LOWER": "attribute"}],
            [{"POS": "NOUN"}, {"LOWER": "attribute"}]])

        self.ENTITY_PATTERNS = [self.CLASS_PATTERN, self.INTERFACE_PATTERN, self.ENUM_PATTERN, self.ATTRIBUTE_PATTERN,
                                self.METHOD_PATTERN]
