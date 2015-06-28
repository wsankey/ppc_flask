import unittest

from project.util import BaseTestCase


class TestMainViews(BaseTestCase):

    def test_main_route_requires_login(self):
        # Ensure main route requres a logged in user.
        response = self.client.get('/', follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertTemplateUsed('user/login.html')


if __name__ == '__main__':
    unittest.main()
