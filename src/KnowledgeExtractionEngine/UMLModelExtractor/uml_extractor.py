import json
import os


class UML_extractor:
    def __init__(self, path_to_solution_file: str):
        if not os.path.isfile(path_to_solution_file):
            raise FileNotFoundError
        with open(path_to_solution_file) as f:
            self.data = json.load(f)
        self.uml_elements = self.get_elements()
        self.uml_relations = self.get_relations()
        self.class_and_interface, self.attributes, self.methods = self.classify_uml_elements(self.uml_elements)

    def get_elements(self) -> list({str: str}):
        uml_elements = self.data["model"]["elements"]
        uml_filtered_elements = [{k: v for k, v in d.items() if k != 'bounds' and k != "owner"} for d in uml_elements]
        return uml_filtered_elements

    def get_relations(self) -> list({str: str}):
        uml_relationships = self.data["model"]["relationships"]
        uml_filtered_relationships = [{k: v for k, v in d.items() if k != 'bounds' and k != "path"} for d in
                                      uml_relationships]
        return uml_filtered_relationships

    def classify_uml_elements(self, uml_elements: list({str: str})) -> (
            list({str: str}), list({str: str}), list({str: str})):
        class_and_interface = list(
            filter(lambda x: x["type"] in {"Class", "Interface", "AbstractClass"}, uml_elements))
        methods = list(filter(lambda x: x["type"] == "ClassMethod", uml_elements))
        attributes = list(filter(lambda x: x["type"] == "ClassAttribute", uml_elements))
        return class_and_interface, attributes, methods

    def join_ids_with_elements(self, item):
        joined_list = item[1]
        if item[0] == "methods":
            joined_list = [list(filter(lambda x: x["id"] == id, self.methods))[0] for id in item[1]]
        elif item[0] == "attributes":
            joined_list = [list(filter(lambda x: x["id"] == id, self.attributes))[0] for id in item[1]]

        return item[0], joined_list

    def join_ids_with_relations(self, relation_dict):
        source = next(filter(lambda element: element["id"] == relation_dict["source"]["element"], self.uml_elements))[
            "name"]
        source_role = relation_dict["source"]["role"]
        target = next(filter(lambda element: element["id"] == relation_dict["target"]["element"], self.uml_elements))[
            "name"]
        target_role = relation_dict["target"]["role"]
        return {"type": relation_dict["type"], "source": source, "target": target, "source_role": source_role,
                "target_role": target_role}

    def map_type_to_relation(self, entity, type):
        new_type = type
        entity_pair = (entity, "")
        if type == "ClassMethod":
            new_type = "method"
        elif type == "ClassAttribute":
            new_type = "attribute"
        elif type == "AbstractClass":
            new_type = "abstract"
            entity_pair = (entity, "class")
        else:
            new_type = type.lower()
        relation = "is " + new_type
        return entity_pair, relation

    def map_class_to_graph(self, entities):
        entity_pairs = []
        relations = []
        for entity in entities:
            class_name = entity["name"]
            class_type = entity["type"]
            type_entity_pair, type_relation = self.map_type_to_relation(class_name, class_type)
            entity_pairs.append(type_entity_pair)
            relations.append(type_relation)

            for att in entity["attributes"]:
                att_name = att["name"].split(":", 1)[0]
                clean_att = att_name[1:]

                entity_pairs.append((clean_att, ""))
                relations.append("is attribute")

                entity_pairs.append((class_name, clean_att))
                relations.append("has attribute")

                entity_pairs.append((clean_att, class_name))
                relations.append("has parent")

            for method in entity["methods"]:
                method_name = ''.join(e for e in method["name"] if e.isalnum())

                entity_pairs.append((method_name, ""))
                relations.append("is method")

                entity_pairs.append((class_name, method_name))
                relations.append("has method")

                entity_pairs.append((method_name, class_name))
                relations.append("has parent")

        return entity_pairs, relations

    def map_relations_to_graph(self, relations):
        relations_dicts = list(map(self.join_ids_with_relations, relations))
        resulting_entity_pairs = []
        resulting_relations = []
        for relation_dict in relations_dicts:
            entity_pairs, relations = self.map_relation_dict_to_graph(relation_dict)
            resulting_entity_pairs.extend(entity_pairs)
            resulting_relations.extend(relations)

        return resulting_entity_pairs, resulting_relations

    def map_relation_dict_to_graph(self, relation_dict):
        entity_pairs = []
        relations = []
        associations = ["ClassBidirectional", "ClassRealization", "ClassComposition", "ClassInheritance",
                        "ClassDependency", "ClassUnidirectional", "ClassAggregation"]
        if relation_dict["type"] == "ClassRealization":
            source = relation_dict["source"]
            target = relation_dict["target"]
            entity_pairs.extend([(source, target), (target, source)])
            relations.extend(["implements", "is implemented by"])
            return entity_pairs, relations
        if relation_dict["type"] == "ClassInheritance":
            source = relation_dict["source"]
            target = relation_dict["target"]
            entity_pairs.extend([(source, target), (target, source)])
            relations.extend(["implements", "is implemented by"])
            return entity_pairs, relations
        if relation_dict["type"] in ["ClassComposition", "ClassAggregation"]:
            source = relation_dict["source"]
            target = relation_dict["target"]
            entity_pairs.extend([(source, target), (target, source)])
            relations.extend(["is composed of", "is part of"])
            return entity_pairs, relations
        if relation_dict["type"] == "ClassDependency":
            source = relation_dict["source"]
            target = relation_dict["target"]
            entity_pairs.extend([(source, target), (target, source)])
            relations.extend(["calls", "is called by"])

            return entity_pairs, relations
        if relation_dict["type"] == "ClassUnidirectional":
            source = relation_dict["source"]
            target = relation_dict["target"]
            target_role = relation_dict["target_role"] if relation_dict["target_role"] != "" else target
            entity_pairs.extend([(source, target_role), (target_role, source)])
            relations.extend(["uses", "is used by"])
            # entity_pairs.extend([(source, target_role), (target_role, source), (target_role, target)])
            # relations.extend(["has attribute", "has parent", "has type"])

            if relation_dict["type"] == "ClassBidirectional":
                source = relation_dict["source"]
                target = relation_dict["target"]
                source_role = relation_dict["source_role"] if relation_dict["source_role"] != "" else source
                target_role = relation_dict["target_role"] if relation_dict["target_role"] != "" else target
                entity_pairs.extend([(source, target_role), (target_role, source)])
                relations.extend("uses", "uses")
                # entity_pairs.extend(
                #   [(source, target_role), (target_role, source), (target_role, target), (target, source_role),
                #   (source_role, target), (source_role, source)])
                # relations.extend(["has attribute", "has parent", "has type", "has attribute", "has parent", "has type"])

        return entity_pairs, relations

    def extract_methods_and_attributes(self):
        entities = [dict(map(lambda item: self.join_ids_with_elements(item), d.items())) for d in
                    self.class_and_interface]

    #
    def get_graph_from_uml_diagram(self):
        classes_with_ids = [dict(map(lambda item: self.join_ids_with_elements(item), d.items())) for d in
                            self.class_and_interface]

        entity_pairs, relations = self.map_class_to_graph(classes_with_ids)
        entity_pairs1, relations1 = self.map_relations_to_graph(self.uml_relations)
        entity_pairs.extend(entity_pairs1)
        relations.extend(relations1)

        return entity_pairs, relations
