from django.test import TestCase

from apps.products.forms import ProductForm
from apps.products.models import Badge


class ProductFormTest(TestCase):

    def test_slug_is_required_when_empty(self):
        form = ProductForm(
            data={
                "title": "Красивое свадебное платье",
                "slug": "",
                "price": "100000",
                "currency": "RUB",
                "availability_status": "in_stock",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("slug", form.errors)

    def test_existing_slug_is_not_replaced(self):
        form = ProductForm(
            data={
                "title": "Красивое свадебное платье",
                "slug": "custom-slug",
                "price": "100000",
                "currency": "RUB",
                "availability_status": "in_stock",
            }
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        self.assertEqual(
            form.cleaned_data["slug"],
            "custom-slug",
        )

class ProductFormSaveTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.badge_a = Badge.objects.create(
            title="Новинка",
            slug="new",
        )

        cls.badge_b = Badge.objects.create(
            title="Хит",
            slug="hit",
        )

    def test_save_assigns_selected_badges(self):
        form = ProductForm(
            data={
                "title": "Платье с бейджами",
                "slug": "dress-with-badges",
                "price": "100000",
                "currency": "RUB",
                "availability_status": "in_stock",
                "badges": [
                    str(self.badge_a.pk),
                    str(self.badge_b.pk),
                ],
            }
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        product = form.save()

        self.assertEqual(
            set(product.badges.all()),
            {self.badge_a, self.badge_b},
        )

    def test_save_without_badges(self):
        form = ProductForm(
            data={
                "title": "Платье без бейджей",
                "slug": "dress-without-badges",
                "price": "120000",
                "currency": "RUB",
                "availability_status": "in_stock",
                "badges": [],
            }
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        product = form.save()

        self.assertEqual(
            product.badges.count(),
            0,
        )