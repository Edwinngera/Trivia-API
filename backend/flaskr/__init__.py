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
    def after_request(response):
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
        return jsonify(
            {
                'success': True,
                'categories':
                {category.id: category.type for category in Category.query.all()}

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
        page = request.args.get('page', 1, type=int)
        start = (page-1)*PER_PAGE
        end = start+PER_PAGE
        questions = [question.format() for question in questions_query]
        p_reponse = questions[start:end]
        return p_reponse

    @app.route('/questions', methods=['GET'])
    def questions():
        selection = Question.query.order_by(Question.id).all()
        questions = paginator(request, selection)
        if len(questions) == 0:
            abort(404)
        else:
            return jsonify(
                {
                    'success': True,
                    'questions': questions,
                    'total_questions': len(selection),
                    'current_category': None,
                    'categories':
                    {category.id: category.type for category in Category.query.all()},
                    'total': len(Question.query.all())

                }
            )

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
        except:
            abort(404)

        return jsonify({
            'success': True
        })
    
    
    

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    
    @app.route('/questions',methods=['POST'])
    def add_question():
        body=request.json
        
        try:
            question_body = body['question']
            answer = body['answer']
            category = body['category']
            difficulty = body['difficulty']
            question=Question(question_body,answer,category,difficulty)
            question.insert()

            print(question.insert())

            return jsonify(
                    {
                    'success': True,
                    'question': question.id

                    }
                )
        except:
                abort(422)

    
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
        body = request.json
        try:
            query = body['searchTerm']
            print(query)
            results = Question.query.filter(
                Question.question.ilike('%' + query + '%')).all()
            questions =  paginator(request, results)
            return jsonify({
                'success': True,
                'questions':questions,
                'total_questions': len(Question.query.all()),
                'current_category': None
            })
        except:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<id>/questions', methods=['GET'])
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def show_questions_in_categorty(id):
        try:
            group = Question.query.order_by(Question.id).filter(Question.category == id).all()
            current_questions =paginator(request,group)

            categories = Category.query.order_by(Category.id).all()  
            return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(group),
            'categories': {category.id: category.type for category in categories},
            'current_category': id 
        })
        except:
            abort(404)

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
            body = request.get_json()
            
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            category_id = quiz_category['id']

            if category_id == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter( Question.id.notin_(previous_questions),Question.category == category_id).all()
            question = None
            if(questions):
                question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': question.format()
            })

        except Exception:
            abort(422)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "The requested resource was not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Sorry, request not processable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "error": 500,
            "message": "Internal server error."
        })

    return app
