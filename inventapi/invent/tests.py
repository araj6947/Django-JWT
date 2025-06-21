from django.test import TestCase
from rest_framework import status

# Create your tests here.
class AppTest(TestCase):
    def test_3_inventory_get_success(self):
        #self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        res=self.client.get('/inventory/items/')
        #print(res.json())
        assert b'[]' in res.content
        assert 200==res.status_code

    def test_4_inventory_post_success(self):
        #self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        res=self.client.post('/inventory/items/',data={'name':'shirt','category':'top wear','price':700,'discount':20,'quantity':2,'barcode':123456})
        #print(res.json())
        assert 'shirt' == res.json()['name']
        assert 201==res.status_code


    def test_5_inventory_delete_success(self):
        #self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        res=self.client.post('/inventory/items/',data={'name':'shirt','category':'top wear','price':700,'discount':20,'quantity':2,'barcode':123456})
        res=self.client.delete('/inventory/items/1/')
        assert 204==res.status_code

    
    def test_6_inventory_post_error(self):
        #self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        res=self.client.post('/inventory/items/',data={'name':'shirt','category':'top wear','price':700,'discount':20,'quantity':2,'barcode':123456})
        res=self.client.post('/inventory/items/',data={'name':'t-shirt','category':'top wear','price':1300,'discount':30,'quantity':2,'barcode':123456})
        #print(res.json())
        assert b'inventory with this barcode already exists' in res.content
        assert 400==res.status_code


    def test_7_inventory_get_sort_success(self):
        #self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        res=self.client.post('/inventory/items/',data={'name':'shirt','category':'top wear','price':700,'discount':20,'quantity':2,'barcode':123456})
        res=self.client.post('/inventory/items/',data={'name':'t-shirt','category':'top wear','price':1300,'discount':30,'quantity':2,'barcode':12345687})
        response=self.client.get('/items/sort/')
        #print(response.json())
        assert 1300==response.json()[0]['price']
        assert 700==response.json()[1]['price']
        assert 200==response.status_code

    def test_8_inventory_get_query_category_success(self):
        #self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        res=self.client.post('/inventory/items/',data={'name':'shirt','category':'top wear','price':700,'discount':20,'quantity':2,'barcode':123456})
        res=self.client.post('/inventory/items/',data={'name':'t-shirt','category':'top wear','price':1300,'discount':30,'quantity':2,'barcode':12345687})  
        res=self.client.post('/inventory/items/',data={'name':'shorts','category':'bottom wear','price':300,'discount':5,'quantity':3,'barcode':123455})
        response=self.client.get('/items/query/top%20wear/')
        print(response.json())
        
        assert 'shirt' in response.json()[0]['name']
        assert 't-shirt' in response.json()[1]['name']
        assert 200==response.status_code
        assert len(response.json())==2