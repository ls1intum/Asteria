from graph_drawer import draw_graph
from itertools import starmap
from tqdm import tqdm

from TextExtractor.parser import Parser
from TextExtractor.sentence_simplifier.sentence_simplifier import sentence_simplifier
from TextExtractor.svo_extractor import get_entities, get_relation


class Text_extractor:
    def __init__(self):
        self.parser = Parser()
        self.simplifier = sentence_simplifier()


    def replace_synonyms(self, entity_pair, relation):
        if "sublcass" or "inherit" in relation:
            relation = "inherit"
            return entity_pair, relation
        if "superclass" in relation:
            entity_pair = entity_pair[1], entity_pair[0]
            relation = "inherit"
            return entity_pair, relation
        # tbd .....


    # solve references
    def get_graph_from_submission(self, txt):
        ref_txt = self.parser.solve_references(txt)

        # simplify and split compound and complex sentences
        sentences = self.simplifier.simplify_sentences(ref_txt)
        print(f"sentences= {sentences}")

        # extract entities and relations
        entity_pairs = [get_entities(i) for i in tqdm(sentences)]
        print(f"entities = {entity_pairs}")
        relations = [get_relation(i) for i in tqdm(sentences)]
        print(f"relations = {relations}")

        # Lemmatization and stemming
        relations = self.parser.get_lemmas(relations)
        print(f"relations_lemmata = {relations}")

        # normalize vocabulary
        starmap(self.replace_synonyms, zip(entity_pairs, relations))
        draw_graph(entity_pairs, relations)

        return entity_pairs, relations
