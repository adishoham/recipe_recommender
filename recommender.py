from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from collections import Counter
import json
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from difflib import get_close_matches
import random



custom_stopwords = {
    # units
    "cup", "cups", "tablespoon", "tablespoons", "teaspoon", "teaspoons",
    "pound", "pounds", "ounces",
    # numbers
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "12", "14",

    # modifiers
    "chopped", "cut", "grated", "sliced", "thinly", "finely", "peeled", "large", "fresh",

    # connectors / junk
    "or", "and", "of", "to", "into", "for", "about", "plus",

    # noise tags
    "freesoy", "freetree", "freekosher", "appétit"
}

# Merge with built-in English stopwords
all_stopwords = custom_stopwords.union(ENGLISH_STOP_WORDS)



def get_clean_text(recipe, stop_words = all_stopwords):
    ingredients = recipe.get("ingredients", []) 
    categories = recipe.get("categories", [])
    line = ingredients + categories
    line = " ".join(line).lower()   #lowercasing the text
    clean_line = re.sub(r'[^\w\s]', "", line) #removing punctuation
    words_list = clean_line.split()
    clean_words_list = []
    for word in words_list:
        if word not in stop_words:
            clean_words_list.append(word)   #adding the words if they are not stop words
    return clean_words_list



def make_tf_idf(recipes):
    vectorizer = TfidfVectorizer()
    vectors_2b = []
    for recipe in recipes:
        recipe = get_clean_text(recipe)
        vectors_2b.append(" ".join(recipe)) #making a list of the recipes
    matrix = vectorizer.fit_transform(vectors_2b) #from those recipes, making a tf-idf matrix
    return matrix, vectorizer



def ingredients_based_recommend(ingredients, matrix, vectorizer, recipes):
    ingr_vector = vectorizer.transform([" ".join(ingredients)]) #ingredients is a list of ingredients
    scores = {}
    for i in range (matrix.shape[0]):
        similarity = cosine_similarity(matrix[i], ingr_vector)[0][0] #messuring how close the ingredients vector to every recipe vector
        scores[i] = similarity
    sorted_dict = sorted(scores, key = scores.get, reverse= True) #sorting the recipes by the level of similarity to the ingredients vector
    counter = 0
    indeces = []
    seen_before = set()
    for index in sorted_dict:
        title = recipes[index].get("title").strip().lower()
        if not title in seen_before:
            seen_before.add(title)
            indeces.append(index)
            counter += 1
        if counter == 5:
            break
    return indeces

            
        


    
def dishes_based_recommend(dishes, matrix, recipes):
    matches_list = []
    titles_list = []
    for rec in recipes:
        title = rec.get("title")
        if title:
            titles_list.append(title.lower())
    for dish in dishes:
        matches = (get_close_matches(dish.lower(), titles_list, n = 1, cutoff=0.5))
        if matches:
            matches_list.append(matches[0])
    indeces_list = []
    for i in range (len(recipes)):
        title =  recipes[i].get("title")
        if title and title.lower() in matches_list:
            indeces_list.append(i)
    vector = matrix[indeces_list].mean(axis = 0)
    vector = np.asarray(vector)
    scores = {}
    for i in range (matrix.shape[0]):
        similarity = cosine_similarity(vector, matrix[i])[0][0]
        scores[i] = similarity
    sorted_dict = sorted(scores, key= scores.get, reverse= True)
    counter = 0
    indeces = []
    seen_before = set()
    for index in sorted_dict:
        title = recipes[index].get("title").strip().lower()
        if not title in seen_before:
            seen_before.add(title)
            indeces.append(index)
            counter += 1
        if counter == 5:
            break
    return indeces
    



def main():
 print("loading recipes...")
 with open('full_format_recipes.json', 'r', encoding='utf-8') as f:
      recipes = json.load(f)
 matrix, vectorizer = make_tf_idf(recipes)
 still_hungry = True
 while(still_hungry):


    user_wish = input("\nhello. i can recommend on a recipe based on ingredients you want or dishes you like.\n" \
    "for ingredients based recommendation press 1.\nfor dishes based recommendation press 2.\n"
    "if you would like to exit, type 3\n")
    if user_wish == "1":
        query = []
        print("type the desired ingredients with 'enter' after each one. type 'exit' when you are done")
        if random.random() < 0.1:
            print("psst psst secret: if you are really into an ingredient, you can type it more than once 😉.")
        user_input = ""
        while user_input != "exit":
            user_input = input("")
            query.append(user_input)
        query.pop()
        top_5 = ingredients_based_recommend(query, matrix, vectorizer, recipes)
        print("Top 5 choices for you:")

        for i in top_5:
            recipe = recipes[i]
            title = recipe.get("title", "No Title")
            ingredients = recipe.get("ingredients", [])
            directions = recipe.get("directions", "No directions provided.")

            print(f"\n🍽️ {title}\n")
            print("🧂 Ingredients:")
            print("\n".join(ingredients))  # prints each ingredient on a new line
            print("\n🧑‍🍳 How to make:\n")
            for i in directions:
                print (i)
            print("\n" + "-"*40)
        
        answer = input("\ndo you wish to exit? type 'y' if you do and anything else if you don't\n")
        if answer == "y" or answer == "Y":
                still_hungry = False
                print ("\nBon appétit, darling!")
            
    
    elif user_wish == "2":
        print("type a dishes you like with 'enter' after each one. type 'exit' when you are done")
        query = []
        user_input = ""
        while user_input != "exit":
            user_input = input("")
            query.append(user_input)
        query.pop()
        top_5 = dishes_based_recommend(query, matrix, recipes)
        print("Top 5 choices for you:")

        for i in top_5:
            recipe = recipes[i]
            title = recipe.get("title", "No Title")
            ingredients = recipe.get("ingredients", [])
            directions = recipe.get("directions", "No directions provided.")

            print(f"\n🍽️ {title}\n")
            print("🧂 Ingredients:")
            print("\n".join(ingredients))  # prints each ingredient on a new line
            print("\n🧑‍🍳 How to make:\n")
            for i in directions:
                print (i)
            print("\n" + "-"*40)
            
        answer = input("\ndo you wish to exit? type 'y' if you do and anything else if you don't\n")
        if answer == "y" or answer == "Y":
                still_hungry = False
                print ("\nBon appétit, darling!")

    elif user_wish == "3":
        print("Bon appétit, darling!")
        still_hungry = False

    else:
        print("invalid input")


if __name__ == "__main__":
    main()







     
