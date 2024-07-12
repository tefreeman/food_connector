# Recipe Ingredient Matcher

## Overview
The Recipe Ingredient Matcher is a system designed to enhance recipe matching and ingredient analysis. It leverages Natural Language Processing (NLP) to parse and quantify ingredients from recipes, calculate probabilities of ingredient matches, and match recipes against a database of ingredients. 

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Recipe Parsing**: Parse ingredients from recipe text to identify and quantify each ingredient.
- **Ingredient Database**: Maintain a comprehensive database of ingredients, including their attributes and nutritional information.
- **Probability Calculation**: Compute the likelihood of ingredient matches using various features and distributions.
- **Server API**: Provide endpoints to fetch random recipes, submit matches, and get ingredient directories.
- **Training Module**: Train the system with match data to improve accuracy of ingredient matching.

## Project Structure
```
- config.ini                  # Configuration file
- measurements.json           # Measurement units data
- main.py                     # Entry point for the application
- helpers.py                  # Helper functions
- nutri.py                    # Nutritional information processor
- probablity.py               # Probability calculation and feature extraction
- parser/                    
  - language_tools.py         # NLP utilities
  - matcher.py                # Ingredient matching logic
  - ingredients_processor.py  # Processor for loading and parsing ingredients
  - recipe.py                 # Recipe feature extraction and suggestions
  - server.py                 # Flask server for API endpoints
  - train.py                  # Training module for probability calculations
  - word.py                   # Word representation and NLP utilities
- README.md                   # Project README file
```

## Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/recipe-ingredient-matcher.git
   cd recipe-ingredient-matcher
   ```

2. **Install Dependencies**
   Ensure that you have Python 3.7 or higher installed. You can use `pip` to install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up MongoDB**
   - Make sure you have MongoDB installed and running on your machine.
   - Configure the MongoDB instance in `config.ini`.

4. **Download NLTK Data**
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('averaged_perceptron_tagger')
   nltk.download('wordnet')
   nltk.download('stopwords')
   ```

## Configuration
You need to configure the database connection and other settings in the `config.ini` file before running the application. Here is an example `config.ini`:
```ini
[Mongo]
uri = mongodb://
ip = localhost
port = 27017
auth = false
username = 
password = 

[Nutritionix_Db]
db_name = nutritionix
food_col_name = food
grocery_col_name = grocery
all_food_col_name = all_food

[Ingredients_Db]
db_name = ingredients
col_processed_name = processed_ingredients

[Recipes_Db]
db_name = recipes
recipes_all_name = all_recipes

[Matches_Db]
db_name = matches
col_matches = matches
```
Update the values according to your local configuration.

## Usage

1. **Start the Server**
   ```bash
   python main.py
   ```
   This will start the Flask server on port `5002`. The application will initialize and load configuration and other resources.

2. **Access Endpoints**
   - **Get Random Recipe**
     ```http
     GET /get_random
     ```
   - **Submit Recipe Match**
     ```http
     POST /submit_recipe_match
     ```
   - **Get Ingredients Directory**
     ```http
     GET /get_ingredients_dir
     ```
   - **Get Ingredients Tree**
     ```http
     GET /get_ingredients_tree
     ```

## Contributing
We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more information.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [NTLK](https://www.nltk.org/) for providing natural language processing functionalities.
- [Pymongo](https://pypi.org/project/pymongo/) for MongoDB interactions.
- [Flask](https://flask.palletsprojects.com/) for building the server and RESTful API endpoints.

Thank you for using Recipe Ingredient Matcher! If you have any questions or issues, feel free to open an issue on GitHub.
