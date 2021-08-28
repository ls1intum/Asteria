import sys

import spacy
# Import the Matcher
from spacy.matcher import Matcher
from TextExtractor.patterns_matcher.entity_pattern_builder import EntityPatternsBuilder
from TextExtractor.patterns_matcher.relation_pattern_builder import RelationPatternBuilder
from TextExtractor.patterns_matcher.semantic_role import semanticRole


class PatternMatcher:
    def __init__(self, nlp):
        self.nlp = nlp
        self.matcher = Matcher(self.nlp.vocab)
        self.load_patterns(EntityPatternsBuilder(), RelationPatternBuilder())

    def load_patterns(self, entity_pattern_builder: EntityPatternsBuilder,
                      relation_pattern_builder: RelationPatternBuilder):
        # Add the pattern to the matcher
        # The first variable is a unique id for the pattern.
        # The second is an optional callback and the third one is our pattern.
        for entity_pattern in entity_pattern_builder.ENTITY_PATTERNS:
            self.matcher.add(entity_pattern.pattern_key, None, *entity_pattern.patterns_values)

        for relation_pattern in relation_pattern_builder.RELATION_PATTERNS:
            self.matcher.add(relation_pattern.pattern_key, None, *relation_pattern.patterns_values)



    def filter_spans(self,spans):
        # Filter a sequence of spans so they don't contain overlaps
        # For spaCy 2.1.4+: this function is available as spacy.util.filter_spans()
        get_sort_key = lambda span: (span.end - span.start, -span.start)
        sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
        result = []
        seen_tokens = set()
        for span in sorted_spans:
            # Check for end - 1 here because boundaries are inclusive
            if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
                result.append(span)
            seen_tokens.update(range(span.start, span.end))
        result = sorted(result, key=lambda span: span.start)
        return result


    def get_semantic_roles_arguments(self, sentence):
        print(f"++++++++ sentence matched: {sentence} +++++++++++++")
        doc = self.nlp(sentence)
        # Use the matcher on the doc
        matches = self.matcher(doc)
        semantic_roles = []
        for match_id, start, end in matches:
            label = self.nlp.vocab.strings[match_id]
            text = doc[start:end].text
            self.filter_spans([doc[start:end]])
            semantic_role = semanticRole(text, start, end, label)
            semantic_roles.append(semantic_role)
            print(f"LABEL = {label} **** TEXT = {text}\n")
        return semantic_roles


