import spacy
import neuralcoref


class Parser:
    def __init__(self):
        self.parser = spacy.load('en_core_web_md', disable=['ner', 'textcat'])
        neuralcoref.add_to_pipe(self.parser)

    def solve_references(self, sample_text):
        doc = self.parser(sample_text)
        resolved_text = doc._.coref_resolved
        return resolved_text

    def get_lemmas(self, relations):
        docs = [self.parser(str) for str in relations]
        relations_lemmata_list = [" ".join([token.lemma_ for token in doc]) for doc in docs]
        return relations_lemmata_list
