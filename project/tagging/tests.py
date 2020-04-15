import unittest
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import CustomTag


class CustomTagTests(TestCase):
    def test_valid_slugs(self):
        test_tags = [
            {"name": "programming", "expected_slug": "programming"},
            {"name": "PyCon", "expected_slug": "pycon"},
            {"name": "local storage", "expected_slug": "local-storage"},
            {"name": "PEN testing", "expected_slug": "pen-testing"},
            {"name": "תִּיכְנוּת", "expected_slug": "תיכנות"},
            {"name": " 프로그램 작성", "expected_slug": "프로그램-작성"},
            {"name": "程式设计", "expected_slug": "程式设计"},
            {"name": "برمجة", "expected_slug": "برمجة"},
            {"name": "आनंद", "expected_slug": "आनद"},
            {"name": "лягушачий", "expected_slug": "лягушачий"},
            {"name": "教程", "expected_slug": "教程"},
            {"name": "Inicio r\u00e1pido", "expected_slug": "inicio-r\u00e1pido"},
            {"name": "最后", "expected_slug": "最后"},
            {"name": " 欲求不満", "expected_slug": "欲求不満"},
            {"name": "စမ်းသပ်ခြင်း", "expected_slug": "စမသပခင"},
            {"name": "ฐานข้อมูล", "expected_slug": "ฐานขอมล"},
            {"name": "основы", "expected_slug": "основы"},
            {"name": "אַלגערידאַם", "expected_slug": "אלגערידאם"},
            {"name": "自動化する", "expected_slug": "自動化する"},
            {"name": "sjálfvirkan", "expected_slug": "sjálfvirkan"},
            {"name": "پژوهش ", "expected_slug": "پژوهش"},
            {"name": " గ్రాఫ్", "expected_slug": "గరఫ"},
            {"name": "데이터 베이스", "expected_slug": "데이터-베이스"},
            {"name": "stòran-dàta", "expected_slug": "stòran-dàta"},
        ]

        for entry in test_tags:
            tag = CustomTag(name=entry["name"])
            tag.save()
            self.assertEqual(tag.slug, entry["expected_slug"])

    @unittest.skip('https://github.com/codebuddies/backend/issues/123')
    def test_brahmic_abugida_slugs(self):
        test_tags = [
            {"name": "हिंदी में जानकारी", "expected_slug": "TODO"},
            {"name": "प्रयास है", "expected_slug": "TODO"},
            {"name": "స్వయంచాలక", "expected_slug": "TODO"},
        ]

        for entry in test_tags:
            tag = CustomTag(name=entry["name"])
            tag.save()
            self.assertEqual(tag.slug, entry["expected_slug"])

    def test_invalid_slugs(self):
        invalid_tag_names = [
            "❤🐸",
            "🐸",
            "  %",
            "//",
        ]
        for name in invalid_tag_names:
            with self.assertRaises(ValidationError):
                tag = CustomTag(name=name)
                tag.save()

    def test_duplicates(self):
        tag1 = CustomTag(name='javascript')
        tag1.save()

        # fail if we try to generate more tags with the same slug
        with self.assertRaises(ValidationError):
            tag2 = CustomTag(name='Javascript')
            tag2.save()

        with self.assertRaises(ValidationError):
            tag3 = CustomTag(name='JaVascripT%/')
            tag3.save()
