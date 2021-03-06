import warnings
from asl_data import SinglesData

def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []

    #Get all word sequences
    Xlengths = test_set.get_all_Xlengths()

    for X, lengths in Xlengths.values():
        word_logL = {}
        best_guess = None
        best_logL = float("-inf")

        for word, model in models.items():
            try:
                logL = model.score(X, lengths)
                #Add the log likelihood for the current word
                word_logL[word] = logL

                #Check for best guess
                if logL > best_logL:
                    best_logL = logL
                    best_guess = word
            except:
                #This word is not viable for this model
                word_logL[word] = float("-inf")
                continue

        guesses.append(best_guess)
        probabilities.append(word_logL)

    # return probabilities, guesses
    return probabilities, guesses
