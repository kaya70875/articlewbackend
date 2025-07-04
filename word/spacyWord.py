import spacy

def calculate_similarity_score(word1 : str, word2 : str) -> float:
    """
        Calculate the similarity between two words.
        :param word1: The first word
        :param word2: The second word
        :return: The similarity between the two words
    """

    nlp = spacy.load("en_core_web_sm")

    word1 = nlp(word1)
    word2 = nlp(word2)

    similarity_score = word1.similarity(word2)

    return similarity_score