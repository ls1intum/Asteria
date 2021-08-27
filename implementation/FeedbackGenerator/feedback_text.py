class FeedbackText:
    def __init__(self, **text):
        """
        Initialize the text
        """
        self.ASSOCIATIONS = ["bidirectional", "realization", "composition", "ClassInheritance", "ClassDependency",
                             "ClassUnidirectional", "ClassAggregation"]
        self.CORRECT_ELEMENT_TEXT = "Well done! You described correctly the element "

        self.SUPERFLUOUS_ELEMENT_TEXT = " is superfluous."

        self.CORRECT_ASSOCIATIONS_TEXT = "You covered all associations for the element "

        self.MISSING_ASSOCIATION_TEXT = "You forgot to mention the association "

    @staticmethod
    def get_correct_element_feedback(element_type: str, element_name: str) -> str:
        return f"Well done! You described correctly the {element_type} {element_name}!"

    @staticmethod
    def get_missing_element_feedback(element_name: str) -> str:
        return f"You forgot to mention the class  {element_name}!"

    @staticmethod
    def get_superfluous_element_feedback(element_name: str) -> str:
        return f"You have a superfluous class with name {element_name}!"

    @staticmethod
    def get_missing_associations_feedback(element_name: str, missing_associations: [str]) -> str:
        associations_str = ",".join(missing_associations)
        return f"You forgot to mention the following associations {associations_str} in {element_name}!"

    @staticmethod
    def get_superfluous_associations_feedback(element_name: str, superfluous_associations: [str]) -> str:
        associations_str = ",".join(superfluous_associations)
        return f"You have superfluous association  in {element_name}!"

    @staticmethod
    def get_associations_fully_correct_feedback(element_name: str) -> str:
        return f"You correctly covered all associations of {element_name}!"

    @staticmethod
    def get_associations_partially_correct_feedback(element_name: str, correct_associations: [str]) -> str:
        associations = ",".join(correct_associations)
        return f"You correctly covered the associations {associations} in {element_name}!"

    @staticmethod
    def get_correct_methods_feedback(element_name: str) -> str:
        return f"You correctly covered all methods of {element_name}!"

    @staticmethod
    def get_missing_method_feedback(element_name: str, missing_methods: int) -> str:
        if missing_methods == 1:
            return f"One method is missing in {element_name}!"
        return f"{missing_methods} methods are missing in {element_name}!"

    @staticmethod
    def get_superfluous_method_feedback(element_name: str, superfluous_methods: int) -> str:
        if superfluous_methods == 1:
            return f"One superfluous method in {element_name}!"
        return f"{superfluous_methods} superfluous methods in {element_name}!"

    @staticmethod
    def get_correct_attributes_feedback(element_name: str) -> str:
        return f"You correctly covered all attributes of {element_name}!"

    @staticmethod
    def get_missing_attribute_feedback(element_name: str, missing_attributes: int) -> str:
        if missing_attributes == 1:
            return f"One attribute is missing in {element_name}!"
        return f"{missing_attributes} attributes are missing in {element_name}!"

    @staticmethod
    def get_superfluous_attribute_feedback(element_name: str, superfluous_attributes: int) -> str:
        if superfluous_attributes == 1:
            return f"One superfluous attribute in {element_name}!"
        return f"{superfluous_attributes} superfluous attributes in {element_name}!"
