from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_blogly_test'
app.config['SQLALCHEMY_ECHO'] = False



class UserTestCase(TestCase):
    """tests for model for users"""
    def setUp(self):
        """Clean up any existing users"""
        with app.app_context():
            User.query.delete()
            db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction"""
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()

    def test_list(self):
        user = User(first_name = 'amy', last_name = 'kim')
        self.assertEquals(user.first_name, "amy")
        self.assertEquals(user.last_name, "kim")
    
    def test_submit_data(self):
        with app.test_client() as client:
            user = User(first_name = 'amy', last_name = 'kim')

            with app.app_context():
                db.session.add(user)
                db.session.commit()

            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('amy kim', html)

    def test_show_user_info(self):
        with app.test_client() as client:
            user = User(first_name = 'milo', last_name = 'kay')

            with app.app_context():
                db.session.add(user)
                db.session.commit()

            resp = client.get('/users/1')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('milo kay', html)
    
    def test_edit_user(self):
        with app.test_client() as client:
            user = User(first_name = 'david', last_name = 'tim')

            with app.app_context():
                db.session.add(user)
                db.session.commit()

                user = User.query.first_or_404()
                resp = client.post(f"/users/{user.id}/edit", follow_redirects = True,
                                data={'first_name': 'samuel', 'last_name': 'jones'})
                html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('samuel jones', html)

    def test_delete_user(self):
         with app.test_client() as client:
            user = User(first_name = 'david', last_name = 'tim')

            with app.app_context():
                db.session.add(user)
                db.session.commit()

            user = User.query.all()
            resp = client.post(f"'/users/{user.id}/delete'", follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)