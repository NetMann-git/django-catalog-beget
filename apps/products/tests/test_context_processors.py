from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory, TestCase

from apps.products.context_processors import (
    comparison_ids,
    recently_viewed_ids,
)


class ComparisonIdsContextProcessorTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_returns_comparison_ids_from_session(self):
        request = self.factory.get("/")
        request.session = SessionStore()
        request.session["comparison"] = [10, 20, 30]

        result = comparison_ids(request)

        self.assertEqual(
            result,
            {
                "comparison_ids": [10, 20, 30],
            },
        )

    def test_returns_empty_list_when_comparison_missing(self):
        request = self.factory.get("/")
        request.session = SessionStore()

        result = comparison_ids(request)

        self.assertEqual(
            result,
            {
                "comparison_ids": [],
            },
        )


class RecentlyViewedIdsContextProcessorTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_returns_recently_viewed_ids_from_session(self):
        request = self.factory.get("/")
        request.session = SessionStore()
        request.session["recently_viewed"] = [30, 20, 10]

        result = recently_viewed_ids(request)

        self.assertEqual(
            result,
            {
                "recently_viewed_ids": [30, 20, 10],
            },
        )

    def test_returns_empty_list_when_recently_viewed_missing(self):
        request = self.factory.get("/")
        request.session = SessionStore()

        result = recently_viewed_ids(request)

        self.assertEqual(
            result,
            {
                "recently_viewed_ids": [],
            },
        )