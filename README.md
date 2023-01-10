# Trivia-API
This API allows users to display, delete, and add questions to a database, as well as search for questions and play a quiz game. All code follows the PEP8 style guide.
## Getting Started ####

### Prerequisites & Installation
#### Backend

To use this API, developers will need the following:

1. **Python 3.7** - Install the latest version of python for your platform using the python documentation.

2. **Virtual Environment** - It is recommended to use a virtual environment when working with Python projects. This helps keep dependencies separate and organized. Follow the python documentation to set up a virtual environment for your platform.

3. **PIP Dependencies** - After setting up your virtual environment, navigate to the /backend directory and install the required dependencies with the following command:
```bash
pip install -r requirements.txt
```

### Set up the Database

First start Postgres and create the trivia database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

Ensure that you are using your virtual environment, and then navigate to the ./src directory. Run the following command to start the server:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

This will allow you to run the flask application in development mode.

#### Frontend

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected. We recommend that you **stand up the backend first**, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

### Unit Tests
To run the unit tests use these commands:
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference
### Getting Started

- Currently this project can onlly be run locally and is not hosted as a base URL. The backend is hosted at the default, http://127.0.0.1:5000, which is set as a proxy in the frontend.
- This version of the API does not require authentication keys.

### Error Handling

Errors are returned as JSON objects in the following format:
```
{
  "success": False,
  "error": 404,
  "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource not found
- 422: Not Processable

### Endpoints

#### GET /categories

- General:
  - Returns a list of category objects as well as a success value


- Sample: ```curl http://127.0.0.1:5000/categories```

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

#### GET /questions

- General:
  - Retrieves all questions in the database paginated every 10 questions.

- Sample ```curl -X GET http://127.0.0.1:5000/questions ```

```
"questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
```

#### DELETE /questions/{id}

- General:
  - Deletes the question of the given ID if it exists. Returns success value.

- Sample ```curl -X DELETE http://127.0.0.1:5000/questions/16?page=2 ```


```
{
  "success": true
}
```

#### POST /questions/{id}


- General:
  - Creates a new question and returns the created questions ID, success value and a list of the current questions paginated every 10 questions

Sample: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who invented thhe telephone?", "answer": "Elon Musk","category" :"1", "difficulty":"5"}'```


```
{
  "created": 100, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "success": true
}
```


#### POST /search


- General:
  - search for a question using the submitted search term. Returns the results, success value, total questions.


- Sample ```curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"Elon"}'```

```
{
  "questions":   
    {
      "answer": "Elon Musk", 
      "category": "1", 
      "difficulty": 5, 
      "id": 17, 
      "question": "Who invented the telepone?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

#### GET /categories/{id}/questions


- General:

  - Returns a list of questions based on given category id as well as current category, total questions and success value
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.


- Sample: ```curl http://127.0.0.1:5000/categories/3/questions```

```
{
  "current_category": 2, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 4
```

**POST /quizzes**

- General:
  - Returns one random question based on given category
  - return the next question in the same category and success value.
  - If no category is given, returns a random question from any category


- Sample``` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Science","id":"1"}, "previous_questions":[13]}'``` 


```
{
  "question": {
    "answer": "Jackson Pollock", 
    "category": 2, 
    "difficulty": 2, 
    "id": 19, 
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  }, 
  "success": true
```

### Authors

Luke Haag and team Udacity

### Acknowledgements

Team Udacity




























