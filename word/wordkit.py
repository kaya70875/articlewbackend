from functools import lru_cache
from nltk.corpus import wordnet
from nltk.corpus import brown
from collections import Counter, defaultdict

class Wordkit:
    def __init__(self, word: str):
        self.word = word.lower()

    def get_word_info_extended(self) -> dict:
        """
        Get information about a word from WordNet, including its definition, synonyms, and examples.
        """
        # Retrieve synsets for the word (could be adjective, adverb, verb, noun, etc.)
        synsets = wordnet.synsets(self.word)
        
        info = {
            "adjective": [],
            "adverb": [],
            "verb": [],
            "noun": [],
            'pos' : self._most_common_pos()
        }
        
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

    @lru_cache(maxsize=1)
    @staticmethod
    def _brown_pos_map() -> dict:
        pos_map = defaultdict(list)
        for w, tag in brown.tagged_words(tagset="universal"):
            pos_map[w.lower()].append(tag.lower())
        return pos_map

    def _most_common_pos(self) -> str | None:
        word_tags = Wordkit._brown_pos_map().get(self.word)
        if not word_tags:
            return None
        
        tag_counts = Counter(word_tags)
        return tag_counts.most_common(1)[0][0].lower()