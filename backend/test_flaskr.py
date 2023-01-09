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
        self.database_path = "postgresql://lukehaag@localhost:5432/{}".format(
            self.database_name
        )
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
    Write at least one test for each test for successful
    operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_category_not_found(self):
        res = self.client().get("/categories/10000")

        self.assertEqual(res.status_code, 404)

    # def test_add_question(self):
    #     new_question = {
    #         "question": "How many apples in apple pie?",
    #         "category": "2",
    #         "answer": "A lot",
    #         "difficulty": 4,
    #     }
    #     res = self.client().post("/questions", json=new_question)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["created"])

    # def test_delete_question(self):
    #     question_to_delete = Question.query.first()
    #     res = self.client().delete(f"/questions/{question_to_delete.id}")
    #     data = json.loads(res.data)
    #
    #     question = Question.query.\
    #         filter(Question.id == question_to_delete.id).one_or_none()
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], question_to_delete.id)
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(len(data['questions']))
    #     self.assertIsNone(question)

    def test_422_delete_non_existing_question(self):
        res = self.client().delete("/questions/4000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_get_question_search_results(self):
        res = self.client().post("/questions/search",
                                 json={"searchTerm": "organ"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertEqual(len(data["questions"]), 1)

    def test_get_question_search_without_results(self):
        res = self.client().post(
            "/questions/search", json={"searchTerm": "funnybananas"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)

    def test_questions_per_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], 1)

    def test_404_category_not_found(self):
        res = self.client().get("/categories/1000/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_play_quiz(self):
        quiz_data = {
            "previous_questions": [],
            "categories": {"type": "Science", "id": 1},
        }
        res = self.client().post("/quizzes", json=quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_play_quiz_random_question_selected(self):
        # Test with valid category and multiple questions available
        quiz_data = {"quiz_category": {"id": 1}}
        res_1 = self.client().post("/quizzes", json=quiz_data)
        data_1 = json.loads(res_1.data)
        print("data", data_1["question"])

        self.assertEqual(res_1.status_code, 200)
        self.assertEqual(data_1["success"], True)
        self.assertIsNotNone(data_1["question"])

        # Test that a different question is returned on second request
        quiz_data = {"quiz_category": {"id": 1}}
        res_2 = self.client().post("/quizzes", json=quiz_data)
        data_2 = json.loads(res_2.data)

        self.assertEqual(res_2.status_code, 200)
        self.assertEqual(data_2["success"], True)
        self.assertIsNotNone(data_2["question"])
        self.assertNotEqual(data_1["question"], data_2["question"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
