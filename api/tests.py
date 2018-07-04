# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
# from django.core.urlresolvers import reverse
from .models import Food

class FoodModelTestCase(TestCase):
    """Food model tests"""

    def setUp(self):
        """Define the test client and other test variables"""
        self.name = "Orange"
        self.calories = 50
        self.food = Food(name=self.name, calories=self.calories)

    def test_model_can_create_a_food(self):
        old_count = Food.objects.count()
        self.food.save()
        new_count = Food.objects.count()
        new_food  = Food.objects.first()

        self.assertNotEqual(old_count, new_count)
        self.assertEqual(new_food.name, self.name)
        self.assertEqual(new_food.calories, self.calories)


class FoodEndpointsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.name = "Orange"
        self.calories = 50
        self.name2 = "Shumai"
        self.calories2 = 350

        self.food = Food(name=self.name, calories=self.calories).save()
        self.food2 = Food(name=self.name2, calories=self.calories2).save()

    def test_food_index_endpoint(self):
        response = self.client.get('/api/v1/foods')
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['name'], self.name)
        self.assertEqual(response.json()[0]['calories'], self.calories)
        self.assertEqual(response.json()[1]['name'], self.name2)
        self.assertEqual(response.json()[1]['calories'], self.calories2)

    def test_food_show_endpoint(self):
        response = self.client.get('/api/v1/foods/2')
        self.assertEqual(response.json()['name'], self.name2)
        self.assertEqual(response.json()['calories'], self.calories2)

    def test_food_create_endpoint(self):
        response = self.client.post('/api/v1/foods', {'name': 'Ramen', 'calories': 650})
        self.assertEqual(response.json()['name'], 'Ramen')
        self.assertEqual(response.json()['calories'], 650)

    def test_food_update_endpoint(self):
        old_food = Food.objects.get(id=1)
        self.assertEqual(old_food.name, self.name)
        self.assertEqual(old_food.calories, self.calories)

        new_name, new_calories = 'Ramen', 650
        response = self.client.patch('/api/v1/foods/1', {'name': new_name, 'calories': new_calories}, format='json')
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['name'], 'Ramen')
        self.assertEqual(response.json()['calories'], 650)

        updated_food = Food.objects.get(id=1)
        self.assertEqual(updated_food.name, new_name)
        self.assertEqual(updated_food.calories, new_calories)
