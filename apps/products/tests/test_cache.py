from django.core.cache import cache
from django.test import TestCase

from apps.products.cache import CatalogCache
from apps.products.cache_keys import (
    CATALOG_FILTERS_KEY,
    CATALOG_QUERYSET_KEY,
)


class CatalogCacheTest(TestCase):

    def setUp(self):
        cache.clear()

    def test_clear_catalog_removes_catalog_queryset_cache(self):
        cache.set(
            CATALOG_QUERYSET_KEY,
            "catalog-data",
        )

        CatalogCache.clear_catalog()

        self.assertIsNone(
            cache.get(CATALOG_QUERYSET_KEY)
        )

    def test_clear_catalog_removes_filters_cache(self):
        cache.set(
            CATALOG_FILTERS_KEY,
            "filters-data",
        )

        CatalogCache.clear_catalog()

        self.assertIsNone(
            cache.get(CATALOG_FILTERS_KEY)
        )

    def test_clear_catalog_removes_both_cache_entries(self):
        cache.set(
            CATALOG_QUERYSET_KEY,
            "catalog-data",
        )

        cache.set(
            CATALOG_FILTERS_KEY,
            "filters-data",
        )

        CatalogCache.clear_catalog()

        self.assertIsNone(
            cache.get(CATALOG_QUERYSET_KEY)
        )

        self.assertIsNone(
            cache.get(CATALOG_FILTERS_KEY)
        )

    def test_clear_catalog_is_safe_when_cache_is_empty(self):
        CatalogCache.clear_catalog()

        self.assertIsNone(
            cache.get(CATALOG_QUERYSET_KEY)
        )

        self.assertIsNone(
            cache.get(CATALOG_FILTERS_KEY)
        )
        