
# Recipe Recommender (CLI)

This is a simple Python-based recipe recommender that runs in the command line. It allows users to get recipe suggestions based on either:

- Ingredients they want to use
- Dishes they already like

The recommendations are based on TF-IDF vectorization and cosine similarity over a dataset of recipes.

---

## Features

- Ingredient-based and dish-based recommendation
- Cleans and processes recipe data with custom stopwords
- Uses TF-IDF to represent recipes as vectors
- Ranks recipes by similarity to user input
- Prevents duplicate recipe results (by title)

---

## How it works

1. Loads a recipe dataset from a JSON file (`full_format_recipes.json`)
2. Cleans and tokenizes the text of each recipe (ingredients + categories)
3. Builds a TF-IDF matrix of all recipes
4. For each user query, constructs a matching vector and compares it to the dataset using cosine similarity
5. Returns the 5 most relevant recipes





