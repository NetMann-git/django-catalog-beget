from django.test import RequestFactory, TestCase

from apps.products.constants import ITEMS_PER_PAGE
from apps.products.models import Product
from apps.products.pagination import CatalogPaginator


class CatalogPaginatorTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.products = [
            Product.objects.create(
                title=f"Платье {index}",
                slug=f"pagination-dress-{index}",
                price=100000 + index,
                is_active=True,
            )
            for index in range(1, ITEMS_PER_PAGE + 3)
        ]

    def setUp(self):
        self.factory = RequestFactory()
        self.queryset = Product.objects.order_by("id")

    def test_first_page(self):
        request = self.factory.get(
            "/catalog/",
            {"page": "1"},
        )

        paginator = CatalogPaginator(
            self.queryset,
            request,
        )

        self.assertEqual(paginator.page_obj.number, 1)
        self.assertEqual(
            len(paginator.page_obj.object_list),
            ITEMS_PER_PAGE,
        )

    def test_second_page(self):
        request = self.factory.get(
            "/catalog/",
            {"page": "2"},
        )

        paginator = CatalogPaginator(
            self.queryset,
            request,
        )

        self.assertEqual(paginator.page_obj.number, 2)
        self.assertEqual(
            len(paginator.page_obj.object_list),
            2,
        )

    def test_query_params_keep_filters_without_page(self):
        request = self.factory.get(
            "/catalog/",
            {
                "page": "2",
                "q": "aurora",
                "brand": "5",
            },
        )

        paginator = CatalogPaginator(
            self.queryset,
            request,
        )

        self.assertIn("q=aurora", paginator.query_params)
        self.assertIn("brand=5", paginator.query_params)
        self.assertNotIn("page=", paginator.query_params)

    def test_context_contains_expected_keys(self):
        request = self.factory.get("/catalog/")

        paginator = CatalogPaginator(
            self.queryset,
            request,
        )

        context = paginator.context()

        self.assertEqual(
            set(context.keys()),
            {
                "products",
                "page_obj",
                "query_params",
            },
        )

        self.assertIs(
            context["page_obj"],
            paginator.page_obj,
        )