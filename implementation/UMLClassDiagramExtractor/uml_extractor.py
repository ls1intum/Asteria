import json

from graph_drawer import draw_graph

control_access_dict = {"+": "public", "-": "private", "#": "protected"}


class UML_extractor:
    def __init__(self, path_to_solution_file):
        with open(path_to_solution_file) as f:
            self.data = json.load(f)

    def get_elements(self):
        uml_elements = self.data["model"]["elements"]
        uml_filtered_elements = [{k: v for k, v in d.items() if k != 'bounds' and k != "owner"} for d in uml_elements]
        return uml_filtered_elements

    def get_relations(self):
        uml_relationships = self.data["model"]["relationships"]
        uml_filtered_relationships = [{k: v for k, v in d.items() if k != 'bounds' and k != "path"} for d in
                                      uml_relationships]
        return uml_filtered_relationships

    def join_ids_with_elements(self, item, methods, attributes):
        joined_list = item[1]
        if item[0] == "methods":
            joined_list = [list(filter(lambda x: x["id"] == id, methods))[0] for id in item[1]]
        elif item[0] == "attributes":
            joined_list = [list(filter(lambda x: x["id"] == id, attributes))[0] for id in item[1]]

        return item[0], joined_list

    def extract_methods_and_attributes(self):
        uml_elements = self.get_elements()

        class_and_interface = list(
            filter(lambda x: x["type"] in {"Class", "Interface", "AbstractClass"}, uml_elements))
        methods = list(filter(lambda x: x["type"] == "ClassMethod", uml_elements))
        attributes = list(filter(lambda x: x["type"] == "ClassAttribute", uml_elements))

        entities = [dict(map(lambda item: self.join_ids_with_elements(item, methods, attributes), d.items())) for d in
                    class_and_interface]

        print(f"entities= {json.dumps(entities, indent=4, sort_keys=True)}\n")

        elements = []
        relations = []
        for item in entities:
            name = item["name"]

            elements.append((name, ""))
            relations.append("be " + item["type"].lower())

            for att in item["attributes"]:
                att_name = att["name"].split(":", 1)[0]
                att_type = att["name"].split(":", 1)[1]
                control_access = control_access_dict[att_name[0]]
                clean_att = att_name[1:]
                elements.append((name, clean_att))
                relations.append("have attribute")
                elements.append((clean_att, ""))
                relations.append(f"is {control_access.lower()}")

            for meth in item["methods"]:
                meth_access = control_access_dict[meth["name"][0]]
                meth_name = meth["name"][2:]
                elements.append((name, meth_name))
                relations.append("have method")
                elements.append((meth_name, ""))
                relations.append(f"be {meth_access}")

        print(f"elements= {elements}")
        print(f"relations= {relations}")

        draw_graph(elements, relations)

        return elements, relations

    def extract_associations(self):
        uml_relations = self.get_relations()
        print(f"relationships= {json.dumps(uml_relations, indent=4, sort_keys=True)}")
        elements, relations = [], []
        return elements,relations

    def get_graph_from_solution(self):
        elements1, relations1 = self.extract_methods_and_attributes()
        elements2, relations2 = self.extract_associations()
        return elements1 + elements2, relations1 + relations2


uml_extractor = UML_extractor(
    "/home/maisa/KnowledgeGraphs/implementation/UMLClassDiagramExtractor/UMLClassDiagram.json")
uml_relations = uml_extractor.extract_associations()
