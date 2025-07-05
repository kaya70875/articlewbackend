from nltk.corpus import wordnet
from nltk.corpus import brown
from collections import Counter

class Wordkit:
    def __init__(self, word):
        self.word = word

    def get_word_info_extended(self) -> dict:
        """
        Get information about a word from WordNet, including its definition, synonyms, and examples.
        
        @params:
        word (str): The word to look up in WordNet.
        @returns:
        dict : A dictionary containing the word's information
        """
        # Retrieve synsets for the word (could be adjective, adverb, verb, noun, etc.)
        synsets = wordnet.synsets(self.word)
        
        # Prepare a dictionary to hold information
        info = {
            "adjective": [],
            "adverb": [],
            "verb": [],
            "noun": [],
            'pos' : self.most_common_pos()
        }
        
        # Loop through each synset to check its part of speech
        for synset in synsets:
            pos = synset.pos()
            word_info = {
                "definition": synset.definition(),
                "synonyms": [lemma.name().replace('_' , ' ') for lemma in synset.lemmas()],
                "examples": synset.examples() if synset.examples() else [],
            }
            
            if pos == 'a':  # Adjective
                info["adjective"].append(word_info)
            elif pos == 'r':  # Adverb
                info["adverb"].append(word_info)
            elif pos == 'v':  # Verb
                info["verb"].append(word_info)
            elif pos == 'n':  # Noun
                info["noun"].append(word_info)
        
        return info

    def most_common_pos(self) -> str:
        """
        Get the most common part of speech for a word.

        @params:
            word (str): The word to look up in the Brown corpus.
        @returns: 
            str: The most common part of speech for the word.
        """
        # Normalize the word to lowercase
        word = self.word.lower()
        
        # Get tagged words from the Brown corpus using the universal tagset
        tagged_words = brown.tagged_words(tagset='universal')
        
        # Filter tags for the specified word
        word_tags = [tag for w, tag in tagged_words if w.lower() == word]
        
        # If the word is not found in the corpus
        if not word_tags:
            return None
        
        # Count the frequency of each tag
        tag_counts = Counter(word_tags)
        
        # Return the most common tag
        return tag_counts.most_common(1)[0][0].lower()