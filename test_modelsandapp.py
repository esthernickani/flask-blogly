from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_blogly_test'
app.config['SQLALCHEMY_ECHO'] = False



class UserTestCase(TestCase):
    """tests for model for users"""
    def setUp(self):
        """Clean up any existing users"""
        db.drop_all()
        db.create_all()

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction"""

        db.session.rollback()

    def test_list(self):
        user = User(first_name = 'amy', last_name = 'kim')
        post = Post(title = 'test', content = 'test content', user_id = 1)

        self.assertEqual(user.first_name, "amy")
        self.assertEqual(user.last_name, "kim")
        self.assertEqual(post.title, "test")
        self.assertEqual(post.content, 'test_content')
    
    def test_submit_data(self):
        with app.test_client() as client:
            user = User(first_name = 'amy', last_name = 'kim')

            db.session.add(user)
            db.session.commit()

            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('amy kim', html)

    def test_show_user_info(self):
        with app.test_client() as client:
            user = User(first_name = 'milo', last_name = 'kay')

            db.session.add(user)
            db.session.commit()
            resp = client.get('/users/1')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('milo kay', html)
    
    def test_edit_user(self):
        with app.test_client() as client:
            user = User(first_name = 'david', last_name = 'tim')

            db.session.add(user)
            db.session.commit()

            user = User.query.first_or_404()
            resp = client.post(f"/users/{user.id}/edit", follow_redirects = True,
                            data={'first_name': 'samuel', 'last_name': 'jones', 'image': ''})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('samuel jones', html)

    def test_delete_user(self):
         with app.test_client() as client:
            user = User(first_name = 'david', last_name = 'tim')

            db.session.add(user)
            db.session.commit()

            user = User.query.all()[0]
            resp = client.post(f"/users/{user.id}/delete", follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

    def test_add_post(self):
        with app.test_client() as client:
            user = User(first_name = 'amy', last_name = 'kim')

            db.session.add(user)
            db.session.commit()

            post = Post(title = 'test', content = 'test content', user_id = 1)
            db.session.add(post)
            db.session.commit()

            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test', html)

    def test_edit_post(self):
        with app.test_client() as client:
            user = User(first_name = 'amy', last_name = 'kim')

            db.session.add(user)
            db.session.commit()

            post = Post(title = 'test', content = 'test content', user_id = 1)
            db.session.add(post)
            db.session.commit()

            post = Post.query.first_or_404()
            resp = client.post(f"/posts/{post.id}/edit", follow_redirects = True, 
                               data={'title': 'edit', 'content': 'edit_content'})
            
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('edit jones', html)
  
            