import unittest
from app import app, db
from models import User

class BloglyTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test client and sample data."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'

        with self.app.app_context():
            db.create_all()

            user1 = User(first_name="Test", last_name="User", image_url="https://via.placeholder.com/150")
            user2 = User(first_name="Another", last_name="User", image_url="https://via.placeholder.com/150")
            db.session.add_all([user1, user2])
            db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_list_users(self):
        """Test the /users route."""
        with self.client as c:
            response = c.get('/users')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test User', response.data)
            self.assertIn(b'Another User', response.data)

    def test_show_user(self):
        """Test the /users/<int:user_id> route."""
        with self.client as c:
            # Test for first user
            response = c.get('/users/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test User', response.data)

            # Test for second user
            response = c.get('/users/2')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Another User', response.data)

    def test_add_user(self):
        """Test the /users/new route."""
        with self.client as c:
            response = c.post('/users/new', data={
                "first_name": "New",
                "last_name": "User",
                "image_url": "https://via.placeholder.com/150"
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'New User', response.data)

    def test_delete_user(self):
        """Test the /users/<int:user_id>/delete route."""
        with self.client as c:
            # Delete first user
            response = c.post('/users/1/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'Test User', response.data)

            # Check if second user is still present
            response = c.get('/users')
            self.assertIn(b'Another User', response.data)

if __name__ == '__main__':
    unittest.main()