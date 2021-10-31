from abc import ABC, abstractmethod


class SimilarityPairs(ABC):
    sources: list
    matrix: list

    @abstractmethod
    def get_similarity_pairs(self, reference_similarity_set: 'SimilarityPairs') -> list:
        pass
