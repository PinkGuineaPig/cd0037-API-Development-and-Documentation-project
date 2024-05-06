import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_NAME, DB_USER, DB_PASSWORD

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, 'localhost:5432', self.database_name)

        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

    
    def tearDown(self):
        """Executed after reach test"""
        pass

      
## -----------------------------------------------------------
## TESTS FOR CATEGORIES
## -----------------------------------------------------------

    def test_get_categories(self):
        """ Checks whether categories can be retrieved and whether they come back in the proper structure """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

        for category_id, category_type in data['categories'].items():
            self.assertTrue(category_id) 
            self.assertTrue(category_type)

    def test_get_question_based_category(self):
        response = self.client().get('/categories/1/questions')
        data = response.get_json()

        self.assertEqual(data['success'],True)
        self.assertEqual(data['currentCategory'][0],"Science")
        self.assertTrue(data['questions'])
        

    def test_404_get_question_beyond_valid_categories(self):
        res = self.client().get('/categories/33/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


## -----------------------------------------------------------
## TESTS FOR QUESTIONS
## -----------------------------------------------------------


    def test_get_questions(self):
        """ Test whether questions are returned for a given page """
        response = self.client().get('/questions?page=1')

        # Continue with JSON parsing only if the response contains data
        if response.data:
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['questions'])
            self.assertTrue(data['totalQuestions'])
            self.assertTrue(data['categories'])
            self.assertFalse(data['currentCategory'])
            self.assertTrue(data['success'])
        else:
            self.fail("No data returned from the API")


    def test_add_question(self):
        """Creates a fake new question, checks whether it got added to the database and deletes it again."""
        with self.app.app_context():
            new_question = {
                'question': 'What is the capital of France?',
                'answer': 'Paris',
                'difficulty': 1,
                'category': 3 
            }

            # Send the POST request
            response = self.client().post('/questions/add', json=new_question)

            # Check if the response content type is application/json
            self.assertEqual(response.content_type, 'application/json')

            # Handle potential JSON decode errors gracefully
            try:
                data = json.loads(response.data)
            except json.JSONDecodeError:
                self.fail("Response is not in valid JSON format.")

            # Asserts to check if the API call was successful
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data.get('success', False), "API should return success=True")
            self.assertIn('created', data, "Response should include 'created'")
            self.assertIn('total_questions', data, "Response should include 'total_questions'")

            # Ensure the number of questions increased by 1
            new_total_questions = Question.query.count()
            self.assertEqual(data['total_questions'], new_total_questions, "Total questions should match the updated count in the database")

            # Retrieve and delete the created entry, ensuring cleanup
            created_entry = Question.query.get(data['created'])
            if created_entry:
                created_entry.delete()
            else:
                self.fail("New question was not added to the database.")

    def test_add_invalid_question(self):
        """Creates an invalid question. Should return a bad request"""
        with self.app.app_context():
            new_invalid_question = {
                'question': '',
                'answer': '',
                'difficulty': 1,
                'category': 3 
            }

            # Send the POST request
            response = self.client().post('/questions/add', json=new_invalid_question)
            body = response.get_json()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(body['message'], "Missing required fields. Provide non-empty question, answer, difficulty, and category.")

    def test_delete_question(self):
        """ Creates a fake entry with and deletes it again to test the deleting procedure """
        with self.app.app_context():
            question = Question(question='Sample Question', answer='Sample Answer', category=1, difficulty=1)
            question.insert()
            id_to_delete = question.id

            # Delete the question
            res = self.client().delete(f'/questions/{id_to_delete}')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['deleted'], id_to_delete)
            self.assertEqual(data['total_questions'], Question.query.count())  # This ensures the total count is as expected after deletion



    def test_get_questions_no_data(self):
        """Tests question retrieval at a non-existent page to provoke an error."""
        response = self.client().get('/questions?page=1000')  # Assuming this page number is out of range
    
        #self.assertEqual(response.content_type, "application/json")
        data = response.get_json()  # Use get_json() which is a method to parse JSON data directly

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)
        self.assertEqual(data['message'], "Pagination Failed")


    def test_search_questions(self):
        """Tests question retrieval """
        search_term = 'Tom Hanks'
        data = {
            'searchTerm' : search_term
        }
        response = self.client().post('/questions/search', json=data, content_type='application/json')
        dat = response.get_json()
        self.assertEqual(201,response.status_code)
        self.assertEqual('Apollo 13',dat['questions'][0]['answer'])


    def test_get_quizz(self):
        res = self.client().post(
            "/quizzes",
            json={
                "quiz_category": {"type": "History", "id": 4},
                "previous_questions": ["2"],
            },
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()