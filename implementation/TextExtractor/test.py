
import spacy
import neuralcoref
from spacy.matcher import Matcher
from TextExtractor.patterns_matcher.entity_pattern_builder import EntityPatternsBuilder
from TextExtractor.patterns_matcher.relation_pattern_builder import RelationPatternBuilder

txt = "The state class is part of the context class. The StartState class implements the State interface. The " \
      "StopState class also implements the State interface. It has the method doAction. "
nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)
entity_pattern_builder = EntityPatternsBuilder()
relation_pattern_builder = RelationPatternBuilder()

entity_pattern = entity_pattern_builder.METHOD_PATTERN
matcher.add(entity_pattern.pattern_key, None, *entity_pattern.patterns_values)
doc = nlp(txt)
matches = matcher(doc)
for match_id, start, end in matches:
      label = nlp.vocab.strings[match_id]
      text = doc[start:end].text
      print(f"LABEL = {label} **** TEXT = {text}\n")