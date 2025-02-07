import spacy

nlp = spacy.load("en_core_web_sm")

def get_word_pos(word: str, sentence:str) -> str:

    """
        Get the part of speech of a word in a sentence.
        :param word: The word to look for
        :param sentence: The sentence to search in

        :return: The part of speech of the word
    """

    # Load the English NLP model
    # Process a sentence
    doc = nlp(sentence)

    # Print POS tags for each token
    for token in doc:
        if token.text == word:
            return token.pos_