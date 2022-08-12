import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv
load_dotenv()



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.DB_HOST = os.getenv('DB_HOST','127.0.0.1:5432')  
        self.DB_USER = os.getenv('DB_USER','postgres')  
        self.DB_PASSWORD = os.getenv('DB_PASSWORD','postgres')  
        self.DB_NAME = os.getenv('TEST_DB','trivia_test') 

        self.database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)


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
        response = self.client().get("/categories")
        #Check status code 
        self.assertEqual(response.status_code, 200)
        #Load response data
        data=json.loads(response)
        #Check whether success==True
        self.assertEqual(data['success'], True)

    # Fetch questions in a category
    def test_fetch_questions_in_category_success(self):
        response = self.client().get('/categories/1/questions')
        # load response data
        data = json.loads(response.data)
        #Check response status 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        #Check number of questions in the cartegory
        self.assertTrue(len(data['questions']))
        #Check total number of questions
        self.assertTrue(data['total_questions'])
        #Check current category
        self.assertTrue(data['current_category'])

    def test_fetch_questions_at_category_failure(self):
         #Fetch questions in category id that doesnt exists
        response = self.client().get('categories/200/questions')
        # load response data
        data = json.loads(response.data)
        # Check response status 
        self.assertEqual(response.status_code, 404)

         #Check whether message is The request is not processable
        self.assertEqual(data['message'], "The requested resource was not found")

        self.assertEqual(data['success'], False)
        

    # Test Delete question endpoint
    def test_delete_question_success(self):
        # create question to be deleted
        question = Question("test", "test", 1, 1)
        question.insert()
        id = question.id
        # delete question and get response
        response = self.client().delete(f"questions/{id}")
        #Check response data
        data = json.loads(response.data)
        #Check response code 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        # check if deleted question no longer exists
        deleted_question = Question.query.get(id)
        self.assertEqual(deleted_question, None)

    def test_delete_non_existent_question(self):

        response = self.client().delete('/questions/200')

        # load response data
        data = json.loads(response.data)
        # Check that response status is equal to 422
        self.assertEqual(response.status_code, 422)

         #Check whether message is The request is not processable
        self.assertEqual(data['message'], "The request is not processable")

        self.assertEqual(data['success'], False)

    # Test search question endpoint
    def test_question_search_success(self):
        query = {
            'searchTerm': 'edwin'
        }
        response = self.client().post('/questions/search', json=query)

        # load response data
        data = json.loads(response.data)
        
        #Check Status code
        self.assertEqual(response.status_code, 200)
        #Check whether success parameter ==True
        self.assertEqual(data['success'], True)
        #Check that question exists
        self.assertIsNotNone(data['questions'])

        self.assertIsNotNone(data['total_questions'])


    #Test Quizzes endpoint
    def test_quiz_success(self):
        quiz = {'previous_questions': [],
                'quiz_category': {'type': 'test', 'id': 2}}

        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        #Check response status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_quiz_failure(self):
        #exclude the previous quetion object from the parameter
        quiz = {'quiz_category': {'type': 'test', 'id': 2}}

        response = self.client().post('/quizzes', json=quiz)
        #Load response data
        data = json.loads(response.data)
        #Check the status of the response
        self.assertEqual(response.status_code, 422)

         #Check whether message is The request is not processable
        self.assertEqual(data['message'], "The request is not processable")


        self.assertEqual(data['success'], False)
 
    #Test questions end point(Adding questions)

    def test_add_question_success(self):

        #create a test question

        question = {
            'question': 'Who was the first president of Kenya?',
            'answer': 'Jomo Kenyatta',
            'category': 4,
            'difficulty': 1
        }
        
        # POST the question
        response = self.client().post('questions', json=question)
        #Checj resposnse data
        data = json.loads(response.data)
        #Check response status
        self.assertEqual(response.status_code, 200)

        self.assertEqual(data['success'], True)

    def test_add_question_failure(self):

        question = {
            'question': 'Who was the first president of Kenya?',
            'answer': 'Jomo Kenyatta',
            'difficulty': 1
        }
       
        # Add question
        response = self.client().post('questions', json=question)
        #Get response data
        data = json.loads(response.data)
        #Check whether the response status code is equal t0 422
        self.assertEqual(response.status_code, 422)
        #Check whether success is equal to false
        self.assertEqual(data['success'], False)
        #Check whether message is The request is not processable
        self.assertEqual(data['message'], "The request is not processable")


    
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
