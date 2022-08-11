import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    CORS(app, resources={r"/*": {"origins": '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request_method(response):

        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')

        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories', methods=['GET'])
    def categories():

        # Get Category response
        question_categories = Category.query.all()

        return jsonify(
            {
                'success': True,
                'categories':
                {category.id: category.type for category in question_categories}

            }
        )
    print(Category.query.all())

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    PER_PAGE = 10

    def paginator(request, questions_query):
        try:
            page = request.args.get('page', 1, type=int)
            begin = (page-1)*PER_PAGE
            end = begin+PER_PAGE

            questions = []

            for question in questions_query:
                questions.append(question.format())

            p_reponse = questions[begin:end]
            return p_reponse
        except Exception as e:
            print(str(e))

    @app.route('/questions', methods=['GET'])
    def questions():
        try:
            questions_query = Question.query.order_by(Question.id).all()
            questions = paginator(request, questions_query)
            qstns= Category.query.all()
            print(qstns)
         
            return_var= jsonify(
                {
                    'success': True,
                    'questions': questions,
                    'total_questions': len(questions),
                    'current_category': None,
                    'categories':
                    {category.id: category.type for category in qstns},
                    'total': len(Question.query.all())

                }
            )
            return return_var
        except Exception as e:
            print(str(e))
                  
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()

            return_var = jsonify({
                'success': True
            })

            return return_var

        except Exception as e:
            abort(404)
            print(str(e))

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def add_question():
        data = request.json

        try:
            body = data['question']#question body
            answer = data['answer']
            category = data['category']
            difficulty = data['difficulty']
            question = Question(body, answer, category, difficulty)
            question.insert() #insert question into the db

            return_var = jsonify({
                'success': True,
                'message': "Question added successfully",
                'question': question.id

            }
            )

            return return_var
        except  Exception as e:
            abort(422)
            print(str(e))

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.json
        try:
            query = data['searchTerm']
            print(query)
            results = Question.query.filter(
                Question.question.ilike('%' + query + '%')).all()
            questions = paginator(request, results)

            total_questions_size = len(Question.query.all())
            return_var = jsonify({
                'success': True,
                'questions': questions,
                'total_questions': total_questions_size,
                'current_category': None
            })
            return return_var
        except Exception as e:
            abort(404)
            print(str(e))

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<id>/questions', methods=['GET'])
    def show_questions_in_categorty(id):
        try:
            questions_group = Question.query.order_by(Question.id).filter(
                Question.category == id).all()
            current_questions = paginator(request, questions_group)

            #get categories and order by Id 
 
            categories = Category.query.order_by(Category.id).all()

            endpoint_response = jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions_group),
                'categories': {category.id: category.type for category in categories},
                'current_category': id
            })

            return endpoint_response
        except Exception as e:
            abort(404)
            print(str(e))

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown wh ether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def get_quiz_questions():
        try:
            #get json data
            data = request.json
            #get previous quesion from the data object
            p_questions = data['previous_questions']
            #get category type 
            cat_type = data['quiz_category']['type']
            #Get category id from the data object
            cat_id = data['quiz_category']['id']
            """
            Check category of id/category type to determine whether the user selects All 
            Clicking on the All link returns the response below
            {'type': 'click', 'id': 0}
            """

            #If the category ty is equal to click, the ALl link has been clicked 
            if cat_type == 'click':
                questions = Question.query.filter(
                    Question.id.notin_(p_questions)).all()
            else:
                questions = Question.query.filter(Question.id.notin_(
                    p_questions).filter(Question.category == cat_id)).all()

            if len(questions) == 0:
                question = None

            else:
                #get a random question in the category
                question = questions[random.randrange(
                    0, len(questions))].format()

            return_var = jsonify({
                'success': True,
                'question': question
            })

            return return_var

        except Exception as e:
            abort(422)
            print(str(e))

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    #Intialize an empty error response object
    error_reponse = {
        'success': "",
        'error': "",
        'message': " "
    }


    @app.errorhandler(422)
    def request_not_processable_handler(error):

        error_reponse['error'] = 422
        error_reponse['success'] = False
        error_reponse['The request is not processable']


        return jsonify({

            error_reponse
        }), 422

    @app.errorhandler(404)
    def resource_not_found_handler(error):

        error_reponse['error'] = 404
        error_reponse['success'] = False
        error_reponse['The requested resource was not found']

        return jsonify({
            error_reponse
        }), 404

  

    @app.errorhandler(400)
    def bad_request_error_handler(error):

        error_reponse['error'] = 400
        error_reponse['success'] = False
        error_reponse['Sorry, Bad  request']

        return jsonify({
            error_reponse
        }), 400

    @app.errorhandler(500)
    def internal_server_error_handler(error):

        error_reponse['error'] = 500
        error_reponse['success'] = False
        error_reponse['Internal server error']

        return jsonify({
            error_reponse
        }), 500

    return app
