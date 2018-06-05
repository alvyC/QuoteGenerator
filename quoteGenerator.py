from nltk.corpus import gutenberg
from collections import defaultdict
import random
import pickle

def buildModel(books):
  model = defaultdict(list)
  for book in books:
    sentences = gutenberg.sents(book)

    for sentence in sentences:
      for i, word in enumerate(sentence):
        if i == len(sentence) - 1:
          model['END'] = model.get('END', []) + [word]
        else:
          if i == 0:
            model['START'] = model.get('START', []) + [word]
          model[word] = model.get(word, []) + [sentence[i+1]]
  return model

def printModel(model):
  bigramFreq = {}
  for key, value in model.items():
    # print(key, " (size) ", len(value), ": " , end = " ")
    bigramFreq[key] = len(value)
    for v in value:
      pass
      # print(v, end = " ")
    # print()
  for key, value in bigramFreq.items():
    # print(key, ": ", value , end = " ")
    pass

  sortedbigramFreq = sorted(bigramFreq, key = bigramFreq.get, reverse = True)

  count = 1
  for r in sortedbigramFreq:
    if count == 20:
      break
    print(r + " " + str(bigramFreq[r]))
    count+=1


def generateQuote(model):
  generated = []
  while True:
      if not generated:
          words = model['START']
      elif generated[-1] in model['END']:
          break
      else:
          words = model[generated[-1]]
      generated.append(random.choice(words))
  print(" ".join(generated))

bookList = gutenberg.fileids()

# has name of the books
austenBooks = []
shakespeareBooks = []
for book in bookList:
  if book.find("shakespeare") != -1:
    shakespeareBooks.append(book)

  if book.find("austen") != -1:
    austenBooks.append(book)

# austen books
# austenModel = buildModel(austenBooks)
# with open("austenModel.txt", "wb") as myFile:
#     pickle.dump(austenModel, myFile)
austenModel = defaultdict(list)
with open("austenModel.txt", "rb") as myFile:
    austenModel = pickle.load(myFile)

# printModel(austenModel)
# print("Austen-like quote: ", end = " ")
print("List of the top ten most frequent bigrams for Jane Austen: ")
generateQuote(austenModel)

# shakespeare books
# shakespeareModel = buildModel(shakespeareBooks)
# with open("shakespeareModel.txt", "wb") as myFile:
#     pickle.dump(shakespeareModel, myFile)
shakespeareModel = defaultdict(list)
with open("shakespeareModel.txt", "rb") as myFile:
    shakespeareModel = pickle.load(myFile)

# printModel(shakespeareModel)
print("List of the top ten most frequent bigrams for Shakespeare: ")
# print("Shakespeare-like quote: ", end = " ")
generateQuote(shakespeareModel)

