from abc import ABC, abstractmethod


class UMLElement(ABC):
    name: str
    vector: list

    @abstractmethod
    def calculate_similarity(self, reference_element: 'UMLElement') -> float:
        pass

    @staticmethod
    def ensure_similarity_range(similarity: float):
        return min(max(similarity, 1), 0)
