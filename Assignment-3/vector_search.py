import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Example code showing how to use spaCy to generate a vector for a string
def example_code():
    # Load the spaCy model
    nlp = spacy.load("en_core_web_sm")

    phrases = ["Hello, world!", "Welcome to spaCy.", "This is an NLP library.", "Embedding phrases with spaCy."]

    for p in phrases:
        n = nlp(p)
        print("Vector for {} is:".format(p))
        print(n.vector) # this gives you the vector for the entire string

# Complete this code to find the top k closest titles to q using vector search
# Use psycopg2 to retrieve the relevant data from the database 
#
# The return format is shown with an example
#
# Note: do not put anything outside this function ... e.g., spacy model should be loaded inside it
# We will be import this function and test it using another python program
#
def find_topk(q, k):
    return [ (i, 'title {}'.format(i)) for i in range(0, k)]

if __name__ == '__main__':
    # comment this out once you have confirmed it works 
    example_code()

    print(find_topk('what is the best relational database?', 5))
