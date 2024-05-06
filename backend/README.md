# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.10.12** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```


### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### API Reference

## Getting Started
  - Backend Base URL: http://127.0.0.1:5000/
  - Frontend Base URL: http://127.0.0.1:3000/

## Error Handling

All errors are defined in the error_handlers.py.
The Errors are returned in the following format:
```json
  {
    "success": False,
    "error": 400,
    "message": "Message"
  }
```

The following errors are prepared:
-   400, handle_bad_request
-   404, handle_not_found_error
-   500, handle_server_error


## Endpoints

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

Example:
```bash
  curl -s http://127.0.0.1:5000/categories | python3 -m json.tool
```

Example Response:
```json
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
---

`GET '/api/v1.0/questions'`

- Fetches questions from the database. The questions are paginated -> 10 Questions per page
- Request Arguments: None
- Returns: An object with a keys: `categories`,`questions`,`keys` and `total_questions`.
- `questions` is a list of questions each with keys:
    -  `answer`
    -  `category`
    -  `difficulty`
    -  `id`
    -  `question`

Example:
```bash
  curl -s http://127.0.0.1:5000/questions | python3 -m json.tool
```

Example Response:
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "currentCategory": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }
    ],
    "success": true,
    "totalQuestions": 19
}
```

***

`DELETE '/questions/int:id'`

- Deletes the question with the given ID from the DB
- Request Arguments: Integer number for the ID
- Returns: An object with a keys: `success`,`deleted`,`total_questions` and `currentCategory`.

Example:
```bash
  curl -X DELETE http://127.0.0.1:5000/questions/43
```

Example Response:
```json
{
  "currentCategory":null,
  "deleted":43,
  "success":true,
  "total_questions":19
}
```

Example Error response, when ID does not exist
```bash
  curl -X DELETE http://127.0.0.1:5000/questions/100000
```
```json
{
  "error":400,
  "message":"Question with ID 100000 not found.",
  "success":false
}
```

---

`POST '/questions`

- Creates a question with the given arguments
- Request Arguments: question, answer, difficulty and category are all mandatory
- Returns: An object with a keys: `created`,`questions`,`success` and `total_questions`.
- questions is a list of dictionaries with the following keys:
  - `answer`
  - `category`
  - `difficulty`
  - `id`
  - `question`

```bash
  curl -X POST -H "Content-Type: application/json" -d '{"question": "What is 4+4?", "answer": "8", "diffic
  ulty": 1, "category": "1"}' http://127.0.0.1:5000/questions/add
```

Example Response:
```json
{
  "created":44,
  "questions":[
      {
        "answer":"Apollo 13",
        "category":5,
        "difficulty":4,
        "id":2,
        "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      },
      {
        "answer":"Tom Cruise",
        "category":5,
        "difficulty":4,
        "id":4,
        "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      },
    ],
    "success":true,
    "total_questions":20
}
```



***

`POST '/questions/search'`

- String to be looked for in the questions table of the DB -> used to search questions
- Request Arguments: String to be looked for
- Returns: A list of all questions matching the input string

Example:
```bash
  curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "What"}' http://127.0.0.1:5000/questions/search
```

Example Response:
```json
{
  "current_category":null,
  "questions":[
    {"answer":"Muhammad Ali",
    "category":4,
    "difficulty":1,
    "id":9,
    "question":"What boxer's original name is Cassius Clay?"
    },
    {
      "answer":"8",
      "category":1,
      "difficulty":1,
      "id":44,
      "question":"What is 4+4?"
    }
    ],
    "total_questions":9
}
```


***

`GET '/categories/int:id/questions'`

- Get questions for a specific category
- Request Arguments: category id
- Returns: A list of all questions corresponding to the chosen category

Example:
```bash
  curl -s http://127.0.0.1:5000/categories/1/questions | python3 -m json.tool
```

Example Response:
```json
{
    "currentCategory": [
        "Science"
    ],
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
        },
        {
            "answer": "8",
            "category": 1,
            "difficulty": 1,
            "id": 44,
            "question": "What is 4+4?"
        }
    ],
    "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
