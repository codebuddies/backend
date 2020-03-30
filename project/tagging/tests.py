from django.test import TestCase
from .models import CustomTag


class CustomTagTests(TestCase):
    def test_slugging(self):
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

            {"name": "हिंदी में जानकारी", "expected_slug": "हद-म-जनकर"},
            {"name": "प्रयास है", "expected_slug": "परयस-ह"},
            {"name": "stòran-dàta", "expected_slug": "stòran-dàta"},
            {"name": "స్వయంచాలక", "expected_slug": "సవయచలక"},

            {"name": "❤", "expected_slug": ""},
            {"name": "🐸", "expected_slug": "_1"},
        ]

        for entry in test_tags:
            tag = CustomTag(name=entry["name"])
            tag.save()
            self.assertEqual(tag.slug, entry["expected_slug"])
