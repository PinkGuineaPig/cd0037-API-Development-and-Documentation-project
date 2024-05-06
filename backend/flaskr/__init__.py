import os
import random
from collections.abc import Mapping
from flask import Flask, request, abort, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Question, Category, db
from error_handlers import register_error_handlers
from werkzeug.exceptions import InternalServerError

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    """ create and configure the app """
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)


    register_error_handlers(app)
    CORS(app)
    cors = CORS(app, resource={r"/api/*": {"origins": "*"}})
    

    @app.after_request
    def after_request(response):
        response.headers.add('Access_Control_Allow_Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access_Control_Allow_Methods',
                             'Get,PUT,POST,DELETE,OPTIONS')
        return response

    def paginate_questions(request, selection):
        """ Splits all questions in pages. Amount of questions per page are controlled by
          the global variable QUESTIONS_PER_PAGE at the top of this file """
        page = request.args.get('page', 1, type=int)
        #page = int(page)
        start = (page-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        els = [el.format() for el in selection]
        current_selection = els[start:end]

        return current_selection

    @app.route('/categories')
    def get_categories():
        """ Sources all categories """
        try:
            cats = db.session.query(Category).order_by(Category.id).all()

            if not cats:
                abort(404)  # No categories found

            # another way to iterate through the result and build a dictionary
            #categories_dict = {}
            #for category in cats:
            #    categories_dict[category.id] = category.type
            
            return jsonify({
                'success': True,
                'categories': {item.id: item.type for item in cats},
                #'total_categories': len(categories_dict)
            }), 200

        except Exception as e:
            raise InternalServerError(description=str(e)) from e


    @app.route('/questions')
    def get_questions():
        """ Retrieves the Questions. Success returns a status code of 200 and failure a status code of 404 """
        try:

            selection = db.session.query(Question).order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()
                        
            if not selection:
                abort(404, description="No questions found")

            current_selection = paginate_questions(request,selection)

            if not current_selection:
                abort(404, description="Pagination Failed")

            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type
            #categories_formatted = [category.format() for category in categories]

            return jsonify({
                'questions': current_selection,
                'totalQuestions': len(selection),
                'categories': categories_dict,
                'currentCategory': None,
                'success': True
            }), 200

        except Exception as e:
            raise e

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """ Deletes a question given an ID. Returns a 404 if the question does not exist.
            In case of success the status code 200 is returned. Every other exception throws a 500 error."""
        try:
            question = Question.query.get(question_id)

            if question is None:
                abort(400,description="Question with ID {} not found.".format(question_id))

            question.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "total_questions": len(Question.query.all()),
                    "currentCategory": None
                }
            ), 200

        except Exception as e:
            raise e

    @app.route('/questions/add',methods=['POST'])
    def new_question():
        """ Adds a new question to the database. In case of missing fields an status code of 400 is returned """
        body = request.get_json()

        if not body:
            abort(400,description="No data provided.")

        question = body.get('question',None)
        answer = body.get('answer',None)
        difficulty = body.get('difficulty',None)
        category = body.get("category", None)
        search = body.get("searchTerm", None)

            # Check if any required field is empty or None
        if not all([question and question.strip(), answer and answer.strip(), difficulty, category]):
            abort(400, description="Missing required fields. Provide non-empty question, answer, difficulty, and category.")

        try:

            new_question = Question(
                question = question,
                answer = answer,
                category = category,
                difficulty = difficulty,
            )
        
            new_question.insert()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request,selection)
            return jsonify({
                'success': True,
                'created': new_question.id,
                'total_questions': Question.query.count(),
                'questions': current_questions
            }), 201

        except Exception as e:
            abort(500, description=str(e))


    @app.route('/questions/search',methods=['POST'])
    def search_question():
        """ Triggers a search in the DB given a word in the search bar """
        body = request.get_json()
        search_term = body.get('searchTerm',None)

        results = []
        if len(search_term):
            results = Question.query.filter(Question.question.ilike('%{term}%'.format(term=search_term))).all()

        return jsonify({
                'questions': [question.format() for question in results],
                'total_questions': len(results),
                'current_category': None
        }), 201


    @app.route('/categories/<int:category_id>/questions')
    def get_question_based_category(category_id):
        
        try:
            questions = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
        
            if not questions:
                abort(404,description="Category with ID {} not found. Or no questions for given category".format(category_id))
        
            current_questions = paginate_questions(request, questions)
            categories = Category.query.all()
        
            return jsonify({
                'success': True,
                'questions': current_questions,
                'currentCategory': [cat.type for cat in categories if cat.id == category_id ]
            }),200
        
        except Exception as e:
            raise e


    @app.route('/quizzes',methods=['POST'])
    def get_quizz():
        """ Returns a random question out of the ppol from the given category. Previous_Questions i a list 
        of indices of questions that where already shown."""
        try:
            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
            category_id = quiz_category['id']

            if category_id == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions),Question.category == category_id).all()
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions),Question.category == category_id).all()
            
            question = None
            if(questions):
                #flash("Ready?.", "info")
                question = random.choice(questions)

                return jsonify({
                    'success': True,
                    'question': question.format()
                })
            
            if not questions:  # Check if questions list is empty
                return redirect(url_for('get_questions')) 
            
        except:
            abort(422)

    return app
