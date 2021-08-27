from TextExtractor.templates_matcher.templates_builder import TemplateBuilder
from TextExtractor.patterns_matcher.semantic_role import semanticRole
from itertools import chain
import copy


class TemplateMatcher:
    def __init__(self):
        template_builder = TemplateBuilder()
        self.templates = template_builder.ALL_RELATIONS_TEMPLATES
        self.associations = template_builder.ALL_ASSOCIATIONS

    def good_seq(self, list1, sublist):
        return [x for x in list1 if x in sublist] == sublist

    def map_sentence_to_template(self, sentence_semantic_roles: [semanticRole]):
        labels = [role.label for role in sentence_semantic_roles]
        matched = False
        matched_template = {}
        matched_templates = []
        index = 0

        while not matched and index < len(self.templates):
            template = self.templates[index]
            #template_labels = list(chain.from_iterable(matched_template))
            #print(f"DEBUG: template = {matched_template}")
            #print(f"DEBUG: template_labels = {template_labels}")
            #matched = labels == template_labels
            matched_template = next((temp for temp in template if self.good_seq(labels, list(chain.from_iterable(temp)))), None)
            print(f"Labels = {labels}")
            matched = matched_template is not None
            index += 1

        if matched:
            print(f"matched_template: {matched_template}")
            matched_labels = list(chain.from_iterable(matched_template))
            template_index = 0
            for index, role in enumerate(sentence_semantic_roles):
                if role.label in matched_labels:
                    if matched_template[template_index][role.label] == "":
                        matched_template[template_index][role.label] = role.text
                    type_template = next(
                        filter(lambda template_dict: role.label in list(chain.from_iterable(template_dict)),
                               TemplateBuilder().ALL_TYPES_TEMPLATES), [])
                    print(f"type_template = {type_template}")
                    if type_template:
                        type_template[0][role.label] = role.text
                        matched_templates.append(type_template)
                        print(f"filled_template= {type_template}")
                    template_index += 1

            matched_templates.append(matched_template)

        print(f"matched template in function = {matched_templates}")

        return matched_templates
