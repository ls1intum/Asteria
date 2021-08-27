from TextExtractor.parser import Parser
from TextExtractor.sentence_simplifier.sentence_simplifier import sentence_simplifier
from TextExtractor.patterns_matcher.patterns_matcher import PatternMatcher
from TextExtractor.templates_matcher.templates_matcher import TemplateMatcher
from TextExtractor.graph_mapper import map_to_graph


class TextExtractor:
    def __init__(self):
        self.patterns_matcher = PatternMatcher()
        self.parser = Parser(self.patterns_matcher.nlp)
        self.simplifier = sentence_simplifier()

    # solve references
    def get_graph_from_text(self, txt):
        #ref_txt = self.parser.solve_references(txt)

        # simplify and split compound and complex sentences
        sentences = self.simplifier.simplify_sentences(txt)
       # print("+++++++++++ SENTENCES +++++++++++\n")
        #print(f"sentences= {sentences}")
        #print("+++++++++++++++++++++++++++++++++\n")
        #sentences = [txt]
        semantic_roles = []
        matched_templates = []
        for sentence in sentences:
            templates_matcher = TemplateMatcher()
            semantic_role = self.patterns_matcher.get_semantic_roles_arguments(sentence)
            print(f"debug: semantic = {semantic_role}")
            semantic_roles.append(semantic_role)
            matched_templates.extend(templates_matcher.map_sentence_to_template(semantic_role))

        print("+++++++++++ MATCHED TEMPLATES +++++++++++\n")
        print(f"{matched_templates}")
        print("+++++++++++++++++++++++++++++++++\n")

        entity_pairs, relations = map_to_graph(matched_templates)

        print("+++++++++++ ENTITY PAIRS +++++++++++\n")
        print(f"{entity_pairs}")
        print("+++++++++++++++++++++++++++++++++\n")
        print("+++++++++++ RELATIONS +++++++++++\n")
        print(f"{relations}")
        print("+++++++++++++++++++++++++++++++++\n")
        return entity_pairs, relations



