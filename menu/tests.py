from django.test import TestCase, SimpleTestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .views import *
from .models import Menu, Item, Ingredient
import json
from .forms import MenuForm


class MenuModelTest(TestCase):
    '''Testing creating new menu model'''
    def test_menu_fields(self):
        menu = Menu()
        menu.season = 'Just a test'
        menu.expiration_date = '2020-03-23'
        menu.save()

        new = Menu.objects.get(pk=menu.pk)
        self.assertEqual(new, menu)


class IngredientModelTest(TestCase):
    '''Testing creating an ingredient model'''
    def test_ingredient_model(self):
        ingredient = Ingredient()
        ingredient.name = 'Blueberry'
        ingredient.save()

        new = Ingredient.objects.get(pk=ingredient.pk)
        self.assertEqual(new, ingredient)


class ItemModelTest(TestCase):
    '''Testing creating an item model'''
    def test_item_model(self):
        test_user = User.objects.create_user(
            'meelee'
        )
    
        item = Item(
            name='apple',
            description='apple milk',
            chef=test_user
        )
        item.save()

        new = Item.objects.get(pk=item.pk)
        self.assertEqual(new, item)        


class UrlsTest(SimpleTestCase):
    '''Testing urls'''
    def test_url_menu_list(self):
        url = reverse('menu_list')
        self.assertEqual(resolve(url).func, menu_list)

    def test_url_menu_edit(self):
        url = reverse('menu_edit', args=[1])
        self.assertEqual(resolve(url).func, edit_menu)

    def test_url_menu_detail(self):
        url = reverse('menu_detail', args=[1])
        self.assertEqual(resolve(url).func, menu_detail)

    def test_url_item_detail(self):
        url = reverse('item_detail', args=[1])
        self.assertEqual(resolve(url).func, item_detail)

    def test_url_menu_new(self):
        url = reverse('menu_new')
        self.assertEqual(resolve(url).func, create_new_menu)    


class ViewsTest(TestCase):
    '''Testing views'''
    def setUp(self):
        self.client = Client()
        self.menu_list_url = reverse('menu_list')
        self.menu_detail_url = reverse('menu_detail', args=[1])
        self.create_new_menu_url = reverse('menu_new')
        self.project1 = Menu.objects.create(
            season='Breakfast 1'
        )
        self.menu_edit_url = reverse('menu_edit', args=[1])

    def test_menu_list_GET(self):
        resp = self.client.get(self.menu_list_url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, self.project1.season)

    def test_menu_detail_GET(self):
        resp = self.client.get(self.menu_detail_url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_create_new_menu_GET(self):
        resp = self.client.get(self.create_new_menu_url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')
 
    def test_edit_menu_view(self):
        resp = self.client.get(self.menu_edit_url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')    

    def test_create_new_menu_POST(self):
        self.test_user = User.objects.create_user(
            'leena_lee'
        )
        self.test_item = Item(
            name='milk',
            description='strawberry milk',
            chef=self.test_user
        )
        self.test_item.save()
        resp = self.client.post(self.create_new_menu_url, {
            'season': 'season_test2',
            'items': [self.test_item],
            'expiration_date': '2013-09-09'
        })

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.test_item.name, 'milk')

 
class MenuFormTests(TestCase):
    '''Testing menu form'''
    def test_menu_form_valid_data(self):
        self.test_user = User.objects.create_user(
            'luna_lee'
        )
        self.test_item = Item(
            name='chocolate',
            description='milk swiss chocolate',
            chef=self.test_user
        )
        self.test_item.save()
 
        self.form = MenuForm(data={
            'season': 'season_test',
            'items': [self.test_item],
            'expiration_date': '2023-01-01'
        })
        self.assertTrue(self.form.is_valid())

    def test_menu_form_valid_expiration_date(self):
        self.test_user = User.objects.create_user(
            'lina_sun'
        )
        self.test_item = Item(
            name='mocha',
            description='sweets and candies',
            chef=self.test_user
        )
        self.test_item.save()
 
        self.form = MenuForm(data={
            'season': 'season_test6',
            'items': [self.test_item],
            'expiration_date': '2013-01-01'
        })

        self.assertFalse(self.form.is_valid())
