# Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


# Endpoints

## GET '/categories'
- Fetches a  categories dictionaries with the  keys as  the ids and the string as the  the category
- Request Parameters : None
- Response Body: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

### Questions


## GET '/questions'
#### Sample Request
`curl http://localhost:5000/questions/`
- Fetches a dictionary of questions
- Request Parameters: None
- Response Body: A json object of categories containin a dictionary of categories; the current category; questions in current page (total_questions), a sum total of all questions (total) and a list of questions with the answer, category, difficult and question as key:value pairs.
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
  "success": true, 
  "total": 19, 
  "total_questions": 19
}
```

## GET 'categories/id/questions'
#### Sample Request
`curl http://localhost:5000/categories/1/questions`
- Fetches a dictionary of questions from a category `category_id`
- Request Parameters   : id:`int`
- Response Body: A json object of categories containin a dictionary of categories; the current category; questions in current page (total_questions), a sum total of all questions (total) and a list of questions with the answer, category, difficult and question as key:value pairs.
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

## POST '/questions'
- Adds a new question to the database
- Request parameters : {"question": string, "answer": string, "category": integer, "difficulty": integer}
- Response Body: A json success object
```
{
    'success': True,
'question': question.id
}
```

## DELETE '/questions/<question_id'>


- Deletes a new question of id `question_id` from the database
- Request   parameters : question_id:`int`
- Response  Body: A json success object
```
{
    'success': True
}
```



## POST '/questions/search'
- Fetches all question matching a specified query (case-insensitive)
- Request JSON: {"searchTerm": string}
- Returns: A list of questions
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Manchester United",
      "category": "6",
      "difficulty": 4,
      "id": 1,
      "question": "Which club does Cristiano Ronaldo play for:"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

## POST '/quizzes'
- Returns a list of questions in a category excluding thte previous question
- Request Arguments: `{"quiz_category": {"id": int, "type": string}, "previous_questions": [list  of int]}`
- Returns: A list of questions
```
{
'success': True,
'question': {
        'id': 20,
        'question': "Who is Kenya's Current President",
        'answer': "Uhuru Kenyyata",
        'category': 3,
        'difficulty': 2
    }
}


