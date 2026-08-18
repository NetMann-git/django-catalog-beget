from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory, TestCase

from apps.products.context import CatalogContextBuilder
from apps.products.models import Product

class CatalogContextBuilderTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def get_request(self, query=None, wishlist=None):
        request = self.factory.get(
            "/catalog/",
            query or {},
        )

        request.user = AnonymousUser()
        request.session = SessionStore()

        if wishlist is not None:
            request.session["wishlist"] = wishlist

        return request

    @patch("apps.products.context.CatalogRepository.filters")
    @patch("apps.products.context.CatalogRepository.catalog")
    def test_build_returns_catalog_context(
        self,
        mock_catalog,
        mock_filters,
    ):
        mock_catalog.return_value = []
        mock_filters.return_value = {
            "brands": [],
            "categories": [],
            "silhouettes": [],
            "collections": [],
            "colors": [],
            "availabilities": [],
        }

        request = self.get_request()

        context = CatalogContextBuilder.build(request)

        self.assertIn("products", context)
        self.assertIn("page_obj", context)
        self.assertIn("query_params", context)
        self.assertIn("search_query", context)
        self.assertIn("selected_brand", context)
        self.assertIn("selected_category", context)
        self.assertIn("wishlist_ids", context)

    @patch("apps.products.context.CatalogRepository.filters")
    @patch("apps.products.context.CatalogRepository.catalog")
    def test_build_uses_anonymous_wishlist_from_session(
        self,
        mock_catalog,
        mock_filters,
    ):
        mock_catalog.return_value = []

        mock_filters.return_value = {
            "brands": [],
            "categories": [],
            "silhouettes": [],
            "collections": [],
            "colors": [],
            "availabilities": [],
        }

        request = self.get_request(
            wishlist=[10, 20, 30],
        )

        context = CatalogContextBuilder.build(request)

        self.assertEqual(
            context["wishlist_ids"],
            [10, 20, 30],
        )

    @patch("apps.products.context.CatalogRepository.filters")
    @patch("apps.products.context.CatalogRepository.catalog")
    def test_build_applies_request_filters_and_pagination(
        self,
        mock_catalog,
        mock_filters,
    ):
        mock_catalog.return_value = Product.objects.none()

        mock_filters.return_value = {
            "brands": [],
            "categories": [],
            "silhouettes": [],
            "collections": [],
            "colors": [],
            "availabilities": [],
        }

        request = self.get_request(
            query={
                "q": "Aurora",
                "brand": "5",
                "page": "2",
            },
        )

        context = CatalogContextBuilder.build(request)

        self.assertEqual(
            context["search_query"],
            "Aurora",
        )

        self.assertEqual(
            context["selected_brand"],
            "5",
        )

        self.assertEqual(
            context["query_params"],
            "q=Aurora&brand=5",
        )

        self.assertNotIn(
            "page=",
            context["query_params"],
        )

        self.assertEqual(
            context["wishlist_ids"],
            [],
        )