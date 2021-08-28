from TextExtractor.templates_matcher.templates_builder import TemplateBuilder
from TextExtractor.patterns_matcher.semantic_role import semanticRole
from itertools import chain
import copy


class TemplateMatcher:
    def __init__(self):
        template_builder = TemplateBuilder()
        self.templates_relations = template_builder.ALL_RELATIONS_TEMPLATES
        self.templates_types = template_builder.ALL_TYPES_TEMPLATES
        self.associations = template_builder.ALL_ASSOCIATIONS
        self.types = template_builder.ELEMENT_TYPES

    def good_seq(self, list1, sublist):
        return [x for x in list1 if x in sublist] == sublist

    def flatten(self, t):
        return [item for sublist in t for item in sublist]



    def map_sentence_to_template(self, sentence_semantic_roles: [semanticRole]):
        labels = [role.label for role in sentence_semantic_roles]
        matched_template = {}
        matched_templates = []
        index = 0

        while index < len(self.templates_relations):
            template = self.templates_relations[index]
            print(f"index = {index}\n")
            print(f"template ={template}\n ")
            #matched_template = next((temp for temp in template if self.good_seq(labels, list(chain.from_iterable(temp)))), None)
            #matched = matched_template is not None
            index = index + 1
            for matched_template in template:
                print(f"matched_template: {matched_template}")
                matched_labels = self.flatten([dict.keys() for dict in matched_template])
                print(f"matched lables = {matched_labels}\n")
                semantic_roles = [semantic_role  for semantic_role in sentence_semantic_roles if semantic_role.label in matched_labels ]

                # map the matched template to all its occurences in one sentence

                for idx in range(len(semantic_roles)):
                    matched_semantic_roles = [x for x in semantic_roles[idx : idx + len(matched_labels)]]
                    print(f"matched template roles = .{[x.label for x in matched_semantic_roles]}")
                    if [x.label for x in matched_semantic_roles] == matched_labels :
                        filled_template = []
                        for ind, role in enumerate(matched_semantic_roles):
                            if matched_template[ind][role.label] == "":
                                filled_template.append({role.label: role.text})
                            else:
                                filled_template.append(matched_template[ind])
                        matched_templates.append(filled_template)

        for semantic_role in sentence_semantic_roles:
            filled_template = []
            if semantic_role.label in self.types:
                pos = self.types.index(semantic_role.label)
                matched_template = self.templates_types[pos]
                filled_template.append({semantic_role.label: semantic_role.text})
                filled_template.append(matched_template[1])
                matched_templates.append(filled_template)

        print(f"matched template in function = {matched_templates}")

        return matched_templates





