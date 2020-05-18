import unittest
from rest_framework.exceptions import ValidationError
from resources.factories import ResourceFactory
from factory import PostGenerationMethodCall, LazyAttribute, create, create_batch
from django.test import TestCase
from taggit.managers import TaggableManager
from .models import CustomTag, TaggedItems
from tagging.managers  import CustomTaggableManager
from .serializers import TagsSerializerField



class CustomTagTests(TestCase):

    def setUp(self):
        self.resource_1, self.resource_2 = create_batch(ResourceFactory, 2)


    def test_unicode_slugify(self):
        test_tags = [
            {"name": "programming", "expected_slug": "programming"},
            {"name": "PROGRAMMING", "expected_slug": "programming"},
            {"name": "PyCon", "expected_slug": "pycon"},
            {"name": "PYCON", "expected_slug": "pycon"},
            {"name": "local storage", "expected_slug": "local-storage"},
            {"name": "local-storage", "expected_slug": "local-storage"},
            {"name": "local/storage", "expected_slug": "localstorage"},
            {"name": "PEN testing", "expected_slug": "pen-testing"},
            {"name": "תִּיכְנוּת", "expected_slug": "תיכנות"},
            {"name": " 프로그램 작성", "expected_slug": "프로그램-작성"},
            {"name": "程式设计", "expected_slug": "程式设计"},
            {"name": "برمجة", "expected_slug": "برمجة"},
            {"name": "आनंद", "expected_slug": "आनंद"},
            {"name": "лягушачий", "expected_slug": "лягушачий"},
            {"name":"Система управления базами данных", "expected_slug": "система-управления-базами-данных"},
            {"name": "教程", "expected_slug": "教程"},
            {"name": "Inicio ápido", "expected_slug": "inicio-ápido"},
            {"name": "最后", "expected_slug": "最后"},
            {"name": " 欲求不満", "expected_slug": "欲求不満"},
            {"name":"数据库 管理 系统", "expected_slug":"数据库-管理-系统"},
            {"name": "စမ်းသပ်ခြင်း", "expected_slug": "စမ်းသပ်ခြင်း"},
            {"name": "ฐานข้อมูล", "expected_slug": "ฐานข้อมูล"},
            {"name": "основы", "expected_slug": "основы"},
            {"name": "אַלגערידאַם", "expected_slug": "אלגערידאם"},
            {"name": "自動化する", "expected_slug": "自動化する"},
            {"name":"מאגר מידע ניהול מערכת", "expected_slug":"מאגר-מידע-ניהול-מערכת"},
            {"name": "sjálfvirkan", "expected_slug": "sjálfvirkan"},
            {"name": "پژوهش ", "expected_slug": "پژوهش"},
            {"name": " గ్రాఫ్", "expected_slug": "గ్రాఫ్"},
            {"name": "데이터 베이스", "expected_slug": "데이터-베이스"},
            {"name": "stòran-dàta", "expected_slug": "stòran-dàta"},
            {"name": "የመረጃ ቋት አስተዳደር ስርዓት", "expected_slug": "የመረጃ-ቋት-አስተዳደር-ስርዓት"}
        ]

        for entry in test_tags:
            tag = CustomTag(name=entry["name"])
            tag.save()
            self.assertEqual(tag.slug, entry["expected_slug"])

    def test_brahmic_abugida_slugify(self):
        test_tags = [
                 {"name": "কর্মক্ষমতা পরীক্ষামূলক   ", "expected_slug": "কর্মক্ষমতা-পরীক্ষামূলক"},                         #Bangla
                 {"name": "ડેટાબેઝ મેનેજમેન્ટ સિસ્ટમ", "expected_slug": "ડેટાબેઝ-મેનેજમેન્ટ-સિસ્ટમ"},                 #Gujarati
                 {"name": " हिंदी में जानकारी  ", "expected_slug": "हिंदी-में-जानकारी"},                                           #Hindi
                 {"name": "ಡೇಟಾಬೇಸ್ ನಿರ್ವಹಣಾ ವ್ಯವಸ್ಥೆ", "expected_slug": "ಡೇಟಾಬೇಸ್-ನಿರ್ವಹಣಾ-ವ್ಯವಸ್ಥೆ"},        #Kannada
                 {"name": "ការសម្តែង ការសាកល្បង", "expected_slug": "ការសម្តែង-ការសាកល្បង"},                     #Khmer
                 {"name": "ການປະຕິບັດ ການທົດສອບ", "expected_slug": "ການປະຕິບັດ-ການທົດສອບ"},             #Lao
                 {"name": " စွမ်းဆောင်ရည် စမ်းသပ်ခြင်း  ", "expected_slug": "စွမ်းဆောင်ရည်-စမ်းသပ်ခြင်း"},      #Myanmar
                 {"name": " စွမ်းဆောင်ရည်   စမ်းသပ်ခြင်း  ", "expected_slug": "စွမ်းဆောင်ရည်-စမ်းသပ်ခြင်း"},    #Myanmar ex space
                 {"name": "പ്രകടനം പരിശോധിക്കുന്നു","expected_slug": "പ്രകടനം-പരിശോധിക്കുന്നു" },      #Malayalam
                 {"name":"කාර්ය සාධනය පරීක්ෂා කිරීම","expected_slug":"කාර්ය-සාධනය-පරීක්ෂා-කිරීම" },                      #Sinhala
                 {"name":"தரவுத்தள மேலாண்மை அமைப்பு","expected_slug":"தரவுத்தள-மேலாண்மை-அமைப்பு"},  #Tamil
                 {"name": "స్వయంచాలక", "expected_slug": "స్వయంచాలక"},                                                          #Telugu
                 {"name": "ระบบจัดการฐานข้อมูล", "expected_slug": "ระบบจัดการฐานข้อมูล"},                                  #Thai
                 ]

        for entry in test_tags:
            tag = CustomTag(name=entry["name"])
            tag.save()
            self.assertEqual(tag.slug, entry["expected_slug"])

    def test_invalid_tag_characters(self):
        disallowed = [
            [" हिंदी 🐙में👌 जानकारी 🌄"],                                           #emoji
            ["ડેટાબેઝ  😀 મેનેજમેન્ટ 😶  સિસ્ટમ😿 "],                         #emoticons
            ["စွမ်းဆောင်ရည်  🙵 စမ်းသ❡❢❣❤❥❦❧ပ်ခြင်း🙗🙞"],      #dingbats
            ["🇳🇪ಡೇಟಾಬೇಸ್🇨🇱 ನಿರ್ವಹಣಾ ವ್ಯವಸ್ಥೆ🇲🇩"],               #flags
            ["⑵데Ⓚ이터➈ 베이스⒮ⓑ"],                                        #enclosed letters and numbers
            ["⅀欲𝛀求𝜳不𝝫満"],                                                   #math symbols
            ["ля♋гуш🈺ачи♓й"],                                               #other symbols
            ["⇪אַלגע↪ריד↹אַם⇜⇝"],                                           #arrows
            ["Inicio ♚🂊🂋🁍🁎🁮ápido🁯🁰🀂🀃🀄🀅🀆"],                           #game symbols
            ["s𝆹𝅥𝅯𝆺𝆺𝅥𝆺𝅥𝅮jálfv𝅘𝅥𝅱𝅘𝅥𝅲𝅙𝅚𝅛irkan𝇜"]                                                #music symbols
        ]
        serializer = TagsSerializerField(model_field='tags')

        for tag in disallowed:
            with self.assertRaisesMessage(ValidationError,  'Emoji, pictograps, and symbols are not supported in tags.' ):
                serializer.validate(tag)

    def test_nonstring_tag(self):
        disallowed = [
            [1, "float"],
            ["butterfly", ["toast", "chicken"]],
            ["peanut", ("sunshine",)]
        ]
        serializer = TagsSerializerField(model_field='tags')

        for tag in disallowed:
            with self.assertRaisesMessage(ValidationError, 'All tags must be of type str.'):
                serializer.validate(tag)

    def test_nonlist_tag(self):
        disallowed = [1, "float", ("sunshine","buttercup"), {"loser": "wins"}]
        serializer = TagsSerializerField(model_field='tags')

        for tag in disallowed:
            with self.assertRaisesMessage(ValidationError, 'Expected a list of tag names but got type '):
                serializer.validate(tag)

    def test_duplicate_slug_handling(self):
        '''
        See  https://github.com/jazzband/django-taggit/issues/448#issuecomment-414474054 &
        https://github.com/wagtail/wagtail/issues/4786#issuecomment-426436030 for the expected behavior  when
        django-taggit has TAGGIT_CASE_INSENSITIVE=True.
        '''

        starter_tags = [
            {"name": "programming", "expected_slug": "programming", "expected_name": "programming"},
            {"name": "PyCon", "expected_slug": "pycon", "expected_name": "PyCon"},
            {"name": "local storage", "expected_slug": "local-storage", "expected_name": "local storage"},
            {"name": "PEN testing", "expected_slug": "pen-testing", "expected_name": "PEN testing"},
            {"name": "database system", "expected_slug": "database-system", "expected_name": "database system"},
        ]

        duped_tags = [
                 # DUPE:  all entries below should hand back the starter_tag  'programming' tag
                 {"name": "PROGRAMMING", "expected_slug": "programming", "expected_name": "programming"},
                 {"name": "PrOgRaMmInG", "expected_slug": "programming", "expected_name": "programming"},
                 {"name": "PROgramming", "expected_slug": "programming", "expected_name": "programming"},

                 # DUPE:  all entries below should hand back the starter_tag 'pycon' tag
                 {"name": "PyCon", "expected_slug": "pycon", "expected_name": "PyCon"},
                 {"name": "PYCON", "expected_slug": "pycon", "expected_name": "PyCon"},
                 {"name": "PYcon", "expected_slug": "pycon", "expected_name": "PyCon"},

                 # DUPE:  all entries below should hand back starter_tag 'local-storage' tag
                 {"name": "LOCAL STORAGE", "expected_slug": "local-storage", "expected_name": "local storage"},
                 {"name": "local storage", "expected_slug": "local-storage", "expected_name": "local storage"},
                 {"name": "lOcal Storage", "expected_slug": "localstorage", "expected_name": "local storage"},
                 {"name": "Local Storage", "expected_slug": "localstorage", "expected_name": "local storage"},

                # DUPE:  all entries below should hand back starter_tag 'pen-testing' tag
                {"name": "pen testing", "expected_slug": "pen-testing", "expected_name": "PEN testing"},
                {"name": "PEN TESTING", "expected_slug": "pen-testing", "expected_name": "PEN testing"},
                {"name": "pen TESTING", "expected_slug": "pen-testing", "expected_name": "PEN testing"},
                {"name": "pEn tEstIng", "expected_slug": "pen-testing", "expected_name": "PEN testing"},

                #DUPE:  all entries below should hand back starter_tag 'database-system' tag
                {"name": "DATABASE SYSTEM", "expected_slug": "database-system", "expected_name": "database system"},
                {"name": "Database System", "expected_slug": "database-system", "expected_name": "database system"},
                {"name": "Database SYSTEM", "expected_slug": "database-system", "expected_name": "database system"},
                {"name": "dAtAbAsE sYsTeM", "expected_slug": "database-system", "expected_name": "database system"},
                ]

        #create tags for resource_1 and resource_2
        self.resource_1.tags.add(*(tag['name'] for tag in starter_tags))
        self.resource_2.tags.add(*(tag['name'] for tag in duped_tags))

        #check that the tags created and attached to resource_1 are the expected format
        self.assertEqual(sorted(self.resource_1.tags.names()), sorted(tag['expected_name'] for tag in starter_tags))
        self.assertEqual(sorted(self.resource_1.tags.slugs()), sorted(tag['expected_slug'] for tag in starter_tags))

        #check that the tags for resource_2 use the tags created for resource_1, because they match case-insesitively
        self.assertEqual(sorted(self.resource_1.tags.names()), sorted(self.resource_2.tags.names()))
        self.assertEqual(sorted(self.resource_1.tags.slugs()), sorted(self.resource_2.tags.slugs()))


    def test_unique_together_name_slug_pairs(self):
        '''
        See  https://github.com/jazzband/django-taggit/issues/448#issuecomment-414474054 &
        https://github.com/wagtail/wagtail/issues/4786#issuecomment-426436030 for the expected behavior  when
        django-taggit has TAGGIT_CASE_INSENSITIVE=True.
        '''

        unique_together_tags = [
                #These values slug to the same thing but  the name is unique, so the two are unique together & are saved.
                {"name": "Database: System", "expected_slug": "database-system", "expected_name": "Database: System"},
                {"name": "Database/ System", "expected_slug": "database-system", "expected_name": "Database/ System"},
                {"name": "Database-System", "expected_slug": "database-system", "expected_name": "Database-System"},

                {"name": "pro/gramming", "expected_slug": "programming", "expected_name": "pro/gramming"},
                {"name": "pro*gramming", "expected_slug": "programming", "expected_name": "pro*gramming"},

               {"name": "PRO: GRAMMING", "expected_slug": "pro-gramming", "expected_name": "PRO: GRAMMING"},
               {"name": "pro   gramming", "expected_slug": "pro-gramming", "expected_name": "pro   gramming"},

                {"name": "Local-Storage", "expected_slug": "local-storage", "expected_name": "Local-Storage"},
                {"name": "Local   :Storage", "expected_slug": "local-storage", "expected_name": "Local   :Storage"},

                {"name": "Local/Storage", "expected_slug": "localstorage", "expected_name": "Local/Storage"},
                {"name": "*Local Storage*", "expected_slug": "local-storage", "expected_name": "*Local Storage*"},
        ]

        #add these new tags to resource_1, check to see they are added and *not* treated as dupes
        self.resource_1.tags.add(*(tag['name'] for tag in unique_together_tags))
        tagging_results = sorted((tag['name'], tag["slug"]) for tag in self.resource_1.tags.all_fields())

        self.assertEqual(tagging_results,
                                    sorted((tag['expected_name'], tag['expected_slug']) for tag in unique_together_tags))
