import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # Fetch Category Success
    def test_fetch_cartegories_success(self):
        res = self.client().get("/categories")
        self.assertEqual(res.status_code, 200)

    # Fetch questions in a category
    def test_fetch_questions_in_category_success(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_fetch_questions_at_category_404(self):
        res = self.client().get('categories/200/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Questions  not found')



    # Test Delete question endpoint
    def test_delete_question_success(self):
        # create question to be deleted
        question = Question("test", "test", 1, 1)
        question.insert()
        id = question.id
        # delete question and get response
        res = self.client().delete(f"questions/{id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check if deleted question no longer exists
        deleted_question = Question.query.get(id)
        self.assertEqual(deleted_question, None)

    def test_delete_non_existent_question(self):
        res = self.client().delete('/questions/200')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request can't be processed")


    # Test search question endpoint
    def test_question_search_success(self):
        query = {
            'searchTerm': 'edwin'
        }
        res = self.client().post('/questions/search', json=query)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])


    #Test Quizzes endpoint
    def test_quiz_success(self):
        quiz = {'previous_questions': [],
                'quiz_category': {'type': 'test', 'id': 2}}

        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_quiz_failure(self):
        quiz = {'quiz_category': {'type': 'test', 'id': 2}}

        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request cannot be processed")

    
    #Test questions end point(Adding questions)

    def test_add_question_success(self):
        question = {
            'question': 'Who was the first president of Kenya?',
            'answer': 'Jomo Kenyatta',
            'category': 4,
            'difficulty': 1
        }
        
        # Add question
        res = self.client().post('questions', json=question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_question_failure(self):

        question = {
            'question': 'Who was the first president of Kenya?',
            'answer': 'Jomo Kenyatta',
            'difficulty': 1
        }
       
        # Add question
        res = self.client().post('questions', json=question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Sorry, request cannot be processed")


    
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
