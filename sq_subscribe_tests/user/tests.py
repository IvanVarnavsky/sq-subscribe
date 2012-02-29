from unittest.case import TestCase
from sq_user.baseuser.backends import CustomUserModelBackend

class SimpleTaskTest(TestCase):

    def test_task(self):
        print 'USER: ', CustomUserModelBackend().user_class()
