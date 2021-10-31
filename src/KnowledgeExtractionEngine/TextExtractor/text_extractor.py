import spacy
from KnowledgeExtractionEngine.TextExtractor.parser import Parser
from KnowledgeExtractionEngine.TextExtractor.patterns_matcher.patterns_matcher import PatternMatcher
from KnowledgeExtractionEngine.TextExtractor.sentence_simplifier.sentence_simplifier import sentence_simplifier
from KnowledgeExtractionEngine.TextExtractor.templates_matcher.templates_matcher import TemplateMatcher


class TextExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md", disable=["ner"])
        self.patterns_matcher = PatternMatcher(self.nlp)
        self.parser = Parser(self.patterns_matcher.nlp)
        self.simplifier = sentence_simplifier()

    def get_graph_from_text(self, txt) -> ([(str, str)], [str]):
        """Extract Knowledge Graph from the student's solution given in the form of a a text

        :param txt: text submitted by a student
        :return: List of nodes of the graph [(source, target)] and a List of the edges [relation]
        """
        # solve references
        # ref_txt = self.parser.solve_references(txt)

        # simplify and split compound and complex sentences
        # sentences = self.simplifier.simplify_sentences(txt)
        doc = self.nlp(txt)
        sentences = [sent.text for sent in doc.sents]
        semantic_roles = []
        matched_templates = []

        for sentence in sentences:
            templates_matcher = TemplateMatcher()
            semantic_role = self.patterns_matcher.get_semantic_roles_arguments(sentence)
            semantic_roles.append(semantic_role)
            matched_templates.extend(templates_matcher.map_sentence_to_template(semantic_role))

        entity_pairs, relations = self.__map_to_graph(matched_templates)

        return entity_pairs, relations

    def __map_to_graph(self, templates: [{}]) -> ([(str, str)], [str]):
        """Map the extracted templates to the entities and relations of the graph

            :param templates: templates extracted from the student's submission
            :return: List of nodes of the graph [(source, target)] and a List of the edges [relation]
        """
        elements = []
        relations = ["has method", "has parent", "calls", "uses", "implements", "is composed of", "is part of"]
        opposite_relations = ["has parent", "has method", "is called by", "is used by", "is implemented by",
                              "is part of", "is composed of"]
        for template in templates:
            values = [value for dict in template for key, value in dict.items()]
            source = self.__clean_name(values[0])
            relation = values[1]
            target = self.__clean_name(values[2]) if len(values) == 3 else "class" if relation == "is abstract" else ""
            elements.append((source, relation, target))
            if relation in relations:
                elements.append((target, opposite_relations[relations.index(relation)], source))

        unique_elements = list(set(elements))
        entity_pairs = [(source, target) for (source, relation, target) in unique_elements]
        relations = [relation for (source, relation, target) in unique_elements]
        return entity_pairs, relations

    def __clean_name(self, name: str) -> str:
        """clean the names of the extracted entities

            :param name: name of the extracted entity
            :return: clean name without extra spaces and special characters
        """
        for str in ["class ", " class", " Class", "Class ", "method ", " method", " Method", " Method ", " interface",
                    "interface ", " Interface", "Interface ", " enum", " enum", " Enum", "Enum ", " attribute",
                    "attribute ",
                    " Attribute", "Attribute "]:
            name = name.replace(str, "")
        name = name[0] + name[1:]
        return name
