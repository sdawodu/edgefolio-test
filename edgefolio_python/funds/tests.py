from django.test import TestCase
from .models import Fund, FundImport
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import override_settings
import shutil

TEST_DIR = 'test_data'

# TODO: test details of created funds
class FundTestCase(TestCase):

    def setUp(self):
        self.fund1 = Fund.objects.create(
            name='Test Fund',
            aum=1000000,
            strategy='first',
            inception_date='2021-01-01'
        )
        fund2 = Fund.objects.create(
            name='Test Fund 2',
            aum=2000000,
            strategy='second',
            inception_date='2021-01-01'
        )
        fund3 = Fund.objects.create(
            name='Test Fund 3',
            aum=3000000,
            strategy='second',
            inception_date='2021-01-01'
        )


    def test_list_view(self):
        response = self.client.get(reverse("funds:fund-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), Fund.objects.count())

    def test_list_view_filtered(self):
        response = self.client.get(reverse("funds:fund-list"), {"strategy": "second"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_detail_view(self):
        url = f"{reverse("funds:fund-list")}{self.fund1.id}/"
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], self.fund1.name)

    def test_list_view_html(self):
        response = self.client.get(reverse("funds:fund-list"), HTTP_ACCEPT="text/html")
        self.assertEqual(response.status_code, 200)

@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class FundImportTestCase(TestCase):

    def setUp(self) -> None:
        test_file_contents ="""Name,AUM (USD),Strategy,Inception Date
Test Fund 4,4000000,first,2021-01-01
Test Fund 5,5000000,second,2021-01-01
"""
        broken_test_file_contents ="""Name,AUM (USD),Strategy,Inception Date
Test Fund 6,6000000,first,2021-01-01
Test Fund 7,seven,second,
"""
        self.test_file =  SimpleUploadedFile("fund.csv", bytes(test_file_contents, encoding="utf-8-sig"))
        self.broken_test_file =  SimpleUploadedFile("fund.csv", bytes(broken_test_file_contents, encoding="utf-8-sig")) 

    def tearDown(self) -> None:
            try:
                shutil.rmtree(TEST_DIR)
            except OSError:
                pass

    def test_funds_created(self):
        fund_import = FundImport.objects.create(file=self.test_file)
        self.assertEqual(Fund.objects.count(), 2)
        fund_import.refresh_from_db()

        self.assertEqual(fund_import.status, "success")

            
    def test_funds_created_partial_success(self):
        fund_import = FundImport.objects.create(file=self.broken_test_file)
        self.assertEqual(Fund.objects.count(), 1)
        fund_import.refresh_from_db()

        self.assertEqual(fund_import.status, "partial_success")