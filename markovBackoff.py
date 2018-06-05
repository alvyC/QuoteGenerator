import random
import nltk
from nltk.corpus import gutenberg

class markov(object):
    def __init__(self, corpus, n_grams, min_length):
        """
        corpus = list of string text ["speech1", "speech2", ..., "speechn"]
        n_grams = max sequence length
        min_length = minimum number of next words required for back-off scheme
        """
        self.grams = {}
        self.n_grams = n_grams
        self.corpus = corpus
        self.min_length = min_length
        self.sequences()

    def tokenizer(self, speech, gram):
        """tokenize speeches in corpus, i.e. split speeches into words"""
        tokenized_speech = nltk.word_tokenize(speech)

        if len(tokenized_speech) < gram:
            pass
        else:
            for i in range(len(tokenized_speech) - gram):
                yield (tokenized_speech[i:i + (gram + 1)])

    def sequences(self):
        """
        create all sequences of length up to n_grams
        along with the pool of next words.
        """
        for gram in range(1, self.n_grams + 1):
            dictionary = {}
            for speech in self.corpus:
                for sequence in self.tokenizer(speech, gram):
                    key_id = tuple(sequence[0:-1])

                    if key_id in dictionary:
                        dictionary[key_id].append(sequence[gram])
                    else:
                        dictionary[key_id] = [sequence[gram]]
            self.grams[gram] = dictionary

    def next_word(self, key_id):
        """returns the next word for an input sequence
        but backs off to shorter sequence if length
        requirement is not met.
        """
        for i in range(len(key_id)):
            try:
                if len(self.grams[len(key_id)][key_id]) >= self.min_length:
                    return random.choice(self.grams[len(key_id)][key_id])
            except KeyError:
                pass
        # if the length requirement isn't met, we shrink the key_id
            if len(key_id) > 1:
                key_id = key_id[1:]
        # when we're down to only a one-word sequence,
        #ignore the requirement
        try:
            return random.choice(self.grams[len(key_id)][key_id])
        except KeyError:
            # key does not exist: should only happen when user enters
            # a sequence whose last word was not in the corpus
            # choose next word at random
            return random.choice(' '.join(self.corpus).split())

    def next_key(self, key_id, res):
        return tuple(key_id[1:]) + tuple([res])

    def generate_markov_text(self, start, size=25):
        """"start is a sentence of at least n_grams words"""
        key_id = tuple(nltk.word_tokenize(start))[ - self.n_grams:]
        gen_words = []
        i = 0
        while i <= size:
            result = self.next_word(key_id)
            key_id = self.next_key(key_id, result)
            gen_words.append(result)
            i += 1
        # print(' '.join(gen_words).replace(' .', '.').replace(' ,', ','))


        bigramFreq = {}
        for key, value in self.grams.items():
            # value is a dictionary and k is a tuple

            for k, v in value.items():
                # print(type(k))
                # print(type(v))
                bigramFreq[k] = len(v)

        sortedBigramFreq = sorted(bigramFreq, key = bigramFreq.get, reverse = True)
        i = 1
        for t in sortedBigramFreq:
            print(t, end = " : ")
            print(bigramFreq[t])
            if (i == 10):
                break;
            i+=1

bookList = gutenberg.fileids()

austenBooks = []
shakespeareBooks = []
for book in bookList:
  if book.find("shakespeare") != -1:
    shakespeareBooks.append(book)
  if book.find("austen") != -1:
    austenBooks.append(book)

shakespeareDocs = []
for book in shakespeareBooks:
    sentences = gutenberg.sents(book)
    for wordList in sentences:
        sentence = ' '.join(wordList)
        shakespeareDocs.append(sentence);

austenDocs = []
for book in austenBooks:
    sentences = gutenberg.sents(book)
    for wordList in sentences:
        sentence = ' '.join(wordList)
        austenDocs.append(sentence);



# print(shakespeareDocs[0])
# print(gutenberg.raw("shakespeare-caesar.txt"))
# doc = ['This is your first text', 'and here is your second text.']
# For better results, use large corpora
mark = markov(austenDocs, 2, 2)
print("List of the top ten most frequent bigrams for Jane Austen: ")
# print("Austen-like quote using markov backoff: ", end = " ")
mark.generate_markov_text('type a sentence that has at least n_grams words', size=25)

mark1 = markov(shakespeareDocs, 2, 2)
print("List of the top ten most frequent bigrams for Shakespeare: ")
# print("Shakespeare-like quote using markov backoff: ", end = " ")
mark1.generate_markov_text('type a sentence that has at least n_grams words', size=25)



