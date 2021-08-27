



def map_to_graph(templates: [{}]):
    elements = []
    relations = ["has method", "calls", "uses", "implements", "is composed of", "is part of"]
    opposite_relations = ["has parent", "is called by", "is used by", "is implemented by", "is part of", "is composed of"]
    for template in templates:
        values = [value for dict in template for key, value in dict.items()]
        print(f"Values: {values}")
        source = clean_name(values[0])
        relation = values[1]
        target = clean_name(values[2]) if len(values) == 3 else "class" if relation == "is abstract" else ""
        elements.append((source, relation, target))
        if relation in relations:
            elements.append((target, opposite_relations[relations.index(relation)], source))

    unique_elements = list(set(elements))
    entity_pairs = [(source, target) for (source, relation, target) in unique_elements]
    relations = [relation for (source, relation, target) in unique_elements]
    return entity_pairs, relations


def clean_name(name: str) -> str:
    name = name[0].lower() + name[1:]
    for str in ["class", "Class", "method", "Method", "interface", "Interface", "enum", "Enum", "attribute",
                "Attribute"]:
        name = name.replace(str, "")
    name = name.replace(" ", "")
    return name
