from django.test import SimpleTestCase
from django.urls import reverse, resolve
from financeAPI.views import APIView, API

class SimpleTest(SimpleTestCase):
    def test_view(self):
        assert 1 == 1


class Test_urls_is_resolves(SimpleTestCase):
    def test_resolve(self):
        url = reverse('object')
        print(resolve(url))
        self.assertEqual(resolve(url).func, APIView)