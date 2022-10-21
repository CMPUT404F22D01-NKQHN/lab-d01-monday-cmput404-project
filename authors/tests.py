from django.test import TestCase
from .models import Author

class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.create(display_name = 'test', email = 'test1', password = 'test1', username = 'test1')
        Author.objects.create(display_name = 'test2', email = 'test2', password = 'test2', username = 'test2')

    def test_author(self):
        test1 = Author.objects.get(display_name = 'test')
        test2 = Author.objects.get(display_name = 'test2')
        self.assertEqual(test1.display_name, 'test')
        self.assertEqual(test2.display_name, 'test2')
        
    def test_duplicate_fail(self):
        try:
            test1 = Author.objects.create(display_name = 'test', email = 'test1', password = 'test1', username = 'test1')
            test2 = Author.objects.create(display_name = 'test', email = 'test1', password = 'test1', username = 'test1')
        except:
            pass
        else:
            self.fail("Duplicate author created")
    
    def test_get_all(self):
        all_authors = Author.objects.all()
        self.assertEqual(len(all_authors), 2)
