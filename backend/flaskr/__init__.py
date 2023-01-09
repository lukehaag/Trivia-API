import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# pagination for questions
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    app.app_context().push()

    """
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    # sets up the cors headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    # handles get requests for all available categories
    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.type).all()

        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": {category.id: category.type
                               for category in categories},
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination
    at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    # Handles GET requests to endpoint questions.
    # Returns a list of questions, count of total questions,
    # categories and current category
    @app.route("/questions")
    def retrieve_questions():
        # Retrieves all the questions and  paginate them with 10 per page
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.order_by(Category.type).all()

        if not current_questions:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "categories": {category.id: category.type
                               for category in categories},
                "current_category": None,
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
     the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    # Handles DELETE requests for questions based on ID.
    # Returns deleted question's id, current questions
    # and list of remaining questions
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        # Try to delete question
        # if question does not exist display a 404 error
        try:
            question = Question.query \
                .filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            # Deletes the question and refreshes te page to show updated list
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )

        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question
     will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    # Adds a new question to the trivia database using POST
    @app.route("/questions", methods=["POST"])
    def add_question():
        body = request.get_json()
        # Gets the data based on user input from the form
        new_question = body.get("question")
        new_answer = body.get("answer")
        new_category = body.get("category")
        new_difficulty = body.get("difficulty")
        # Tries to create new question object
        # based on results and inserts it into database
        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty,
            )
            question.insert()
            # Shows an updated list of all the questions
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                }
            )
        except Exception as e:
            print(e)
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

    # Takes in a search term and deletes all questions
    # that are similar to the search term
    @app.route("/questions/search", methods=["POST"])
    def search_question():
        body = request.get_json()
        search = body.get("searchTerm", None)
        # If search contains a value
        # then find all current questions based on a case-insensitive search
        if search:
            current_questions = Question.query.filter(
                Question.question.ilike("%{}%".format(search))
            ).all()

            return jsonify(
                {
                    "success": True,
                    "questions": [question.format() for question in
                                  current_questions],
                    "total_questions": len(current_questions),
                    "current_category": None,
                }
            )

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    # Retrieves all the questions based on a category ID
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def retrieve_by_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        # If questions is empty display 404 error
        if not questions:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": [question.format() for question in questions],
                "total_questions": len(questions),
                "current_category": category_id,
            }
        )

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    # Retrieves the questions to play the quiz
    # Also retrieves the category if applicable as well as previous
    # questions and then chooses a new question based on category
    # and whether the question is in the previous
    # questions list
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        try:
            body = request.get_json()

            category = body.get("quiz_category", {}).get("id")
            previous_questions = body.get("previous_questions")

            # Creates an empty list if previous questions is empty
            if not previous_questions:
                previous_questions = []

            # If category contains a value
            # filter questions based on that category
            # Else fetch all questions
            if category:
                questions = (
                    Question.query.filter(Question.category == category)
                    .filter(Question.id.notin_(previous_questions))
                    .all()
                )

            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)
                ).all()

            if not questions:
                return jsonify(
                    {"success": True, "question": None})

            # Select a random question from
            # list of questions and add it to previous questions
            question = random.choice(questions)
            previous_questions.append(question.id)

            return jsonify(
                {
                    "success": True,
                    "question": question.format(),
                    "previous_questions": previous_questions
                }
            )
        except Exception as e:
            print("Error:", e)
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def not_found(error):
        return (
            jsonify({"success": False,
                     "error": 404, "message": "bad request"}),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False,
                     "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False,
                     "error": 422, "message": "unprocessable"}),
            422,
        )

    return app
