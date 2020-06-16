from unittest import TestCase

from app import app

from models import db, User, Post, Tag

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
        Post.query.delete()
        Tag.query.delete()

        user = User(first_name="Bob", last_name="Smith", image_url="https://not.a.website")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        post = Post(title="test title", content="test content", user_id=self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

        tag = Tag(name="test tag")
        db.session.add(tag)
        db.session.commit()
        self.tag_id = tag.id

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
            self.assertIn('SUBMIT', html)

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
            self.assertIn('test title', html)
            self.assertIn('EDIT', html)
            self.assertIn('DELETE', html)
            self.assertIn('ADD POST', html)
            


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

    def test_user_posts(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)
            inputCount = html.count('<input')
            textAreaCount = html.count('/textarea')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(inputCount, 2)
            self.assertEqual(textAreaCount, 1)
            self.assertIn('title', html)
            self.assertIn('content', html)
            self.assertIn('ADD', html)
            self.assertIn('CANCEL', html)

    def test_create_user_posts(self):
        with app.test_client() as client:
            d = {'post-title': 'test title two', 'post-content':'test content two', 'user_id': self.user_id}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test title', html)
            self.assertIn('test title two', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test title', html)
            self.assertIn('test content', html)
            self.assertIn('EDIT', html)
            self.assertIn('DELETE', html)

    def test_edit_post_form(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('EDIT POST', html)
            self.assertIn('TITLE', html)
            self.assertIn('CONTENT', html)
            self.assertIn('test title', html)
            self.assertIn('test content', html)

    def test_edit_post(self):
        with app.test_client() as client:
            d = {"post-title": "edited test title", "post-content": "edited test content"}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('edited test title', html)
            self.assertIn('edited test content', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn("test title", html)

    def test_tags(self):
        with app.test_client() as client:
            resp = client.get(f"/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TAGS", html)
            self.assertIn("test tag", html)
            self.assertIn("CANCEL", html)
            self.assertIn("ADD TAG", html)

    def test_single_tag(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test tag", html)
            self.assertIn("CANCEL", html)
            self.assertIn("EDIT", html)

    def test_add_tag_form(self):
        with app.test_client() as client:
            resp = client.get('/tags/new')
            html = resp.get_data(as_text=True)
            inputCount =  html.count('input')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(inputCount, 1)
            self.assertIn('Create a Tag', html)
            self.assertIn('Name', html)
            self.assertIn('CANCEL', html)
            self.assertIn('ADD', html)


    def test_add_tag(self):
        with app.test_client() as client:
            d = {'tag-name': 'test tag two'}
            resp = client.post('/tags/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            liCount = html.count('<li>')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(liCount, 2)
            self.assertIn('test tag two', html)

    






# GET /tags/[tag-id]/edit
# Show edit form for a tag.
# POST /tags/[tag-id]/edit
# Process edit form, edit tag, and redirects to the tags list.
# POST /tags/[tag-id]/delete
# Delete a tag.