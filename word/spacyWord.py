import spacy

def get_word_pos(word: str, sentence:str) -> str:

    """
        Get the part of speech of a word in a sentence.
        :param word: The word to look for
        :param sentence: The sentence to search in

        :return: The part of speech of the word
    """

    nlp = spacy.load("en_core_web_sm")

    # Load the English NLP model
    # Process a sentence
    doc = nlp(sentence)

    # Print POS tags for each token
    for token in doc:
        if token.text == word:
            return token.pos_

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