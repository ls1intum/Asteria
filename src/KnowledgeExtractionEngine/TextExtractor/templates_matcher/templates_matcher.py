from KnowledgeExtractionEngine.TextExtractor.patterns_matcher.semantic_role import semanticRole
from KnowledgeExtractionEngine.TextExtractor.templates_matcher.templates_builder import TemplateBuilder


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

    def fill_template(self, matched_template, matched_semantic_roles) -> [dict]:
        """fill the matched template with the corresponding spans of text from a sentence

            :param matched_semantic_roles: The matched sentence
            :param matched_template: The matched template
            :return: List containing dictionaries,
            each dictionary contains a key with is the label of the template and the value which is the corresponding
            span of text
        """
        filled_template = []
        for ind, role in enumerate(matched_semantic_roles):
            if matched_template[ind][role.label] == "":
                filled_template.append({role.label: role.text})
            else:
                filled_template.append(matched_template[ind])
        return filled_template

    def map_sentence_to_template(self, sentence_semantic_roles: [semanticRole]) -> [[dict]]:
        """map sentence to predefined templates

            :param sentence_semantic_roles:
            :return: List containing all matched templates for a specific sentence
        """
        matched_templates = []
        index = 0

        while index < len(self.templates_relations):
            template = self.templates_relations[index]
            index = index + 1
            for matched_template in template:
                matched_labels = self.flatten([dict.keys() for dict in matched_template])
                semantic_roles = [semantic_role for semantic_role in sentence_semantic_roles if
                                  semantic_role.label in matched_labels]

                # map the matched template to all its occurences in one sentence

                for idx in range(len(semantic_roles)):
                    matched_semantic_roles = [x for x in semantic_roles[idx: idx + len(matched_labels)]]

                    if [x.label for x in matched_semantic_roles] == matched_labels:
                        filled_template = self.fill_template(matched_template, matched_semantic_roles)
                        matched_templates.append(filled_template)

        for semantic_role in sentence_semantic_roles:
            filled_template = []
            if semantic_role.label in self.types:
                pos = self.types.index(semantic_role.label)
                matched_template = self.templates_types[pos]
                filled_template.append({semantic_role.label: semantic_role.text})
                filled_template.append(matched_template[1])
                matched_templates.append(filled_template)

        return matched_templates
