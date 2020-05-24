from unittest import TestCase

from app import app

from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_tests'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()





class bloglyViewsTestCase(TestCase):
    """Tests for Blogly app views"""

    def setUp(self):
        """Add test user"""

        User.query.delete()

        user = User(first_name="Bob", last_name="Smith", image_url="https://not.a.website")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """clean out the junk when we're done"""
        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Bob', html)

    def test_users_list(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Bob', html)
            self.assertIn('Add User', html)

    def test_new_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)
            inputCount = html.count('input')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(inputCount, 3)
            self.assertIn('Submit', html)

    def test_add_new_user(self):
        with app.test_client() as client:
            d = {"firstname": "Henry", "lastname": "Hill", "imageurl": "https://still.not.real"}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Henry', html)
            self.assertIn('Hill', html)

    def test_user_info(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Bob', html)
            self.assertIn('Smith', html)
            self.assertIn('EDIT', html)
            self.assertIn('DELETE', html)

    def test_edit_user_form(self):
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)
            inputCount = html.count('input')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(inputCount, 3)
            self.assertIn('Bob', html)
            self.assertIn('Smith', html)
            self.assertIn('SUBMIT', html)
            self.assertIn('CANCEL', html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"firstname": "Robert", "lastname": "Smithy", "imageurl": "nope"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Robert", html)
            self.assertIn("Smithy", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Bob", html)
            self.assertNotIn("Smith", html)