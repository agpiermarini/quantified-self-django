# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Food, Meal
# from django.core.urlresolvers import reverse

class FoodModelTestCase(TestCase):

    def setUp(self):
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
        response = self.client.post('/api/v1/foods', {'food': {'name': 'Ramen', 'calories': 650}}, format='json')
        self.assertEqual(response.json()['name'], 'Ramen')
        self.assertEqual(response.json()['calories'], 650)

    def test_food_update_endpoint_put(self):
        old_food = Food.objects.get(id=1)
        self.assertEqual(old_food.name, self.name)
        self.assertEqual(old_food.calories, self.calories)

        new_name, new_calories = 'Ramen', 650
        response = self.client.put('/api/v1/foods/1', {'food': {'name': 'Ramen', 'calories': 650}}, format='json')
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['name'], 'Ramen')
        self.assertEqual(response.json()['calories'], 650)

        updated_food = Food.objects.get(id=1)
        self.assertEqual(updated_food.name, new_name)
        self.assertEqual(updated_food.calories, new_calories)

    def test_food_update_endpoint_patch(self):
        old_food = Food.objects.get(id=1)
        self.assertEqual(old_food.name, self.name)
        self.assertEqual(old_food.calories, self.calories)

        new_name, new_calories = 'Ramen', 650
        response = self.client.patch('/api/v1/foods/1', {'food': {'name': 'Ramen', 'calories': 650}}, format='json')
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['name'], 'Ramen')
        self.assertEqual(response.json()['calories'], 650)

        updated_food = Food.objects.get(id=1)
        self.assertEqual(updated_food.name, new_name)
        self.assertEqual(updated_food.calories, new_calories)

    def test_food_delete_endpoint(self):
        self.assertEqual(len(Food.objects.all()), 2)

        response = self.client.delete('/api/v1/foods/1')
        self.assertEqual(len(Food.objects.all()), 1)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(status.is_success(response.status_code))

class MealModelTestCase(TestCase):

    def setUp(self):
        self.meal_name = "Breakfast"
        self.meal = Meal(name=self.meal_name)
        self.food = Food(name="Coffee", calories=50).save()

    def test_model_can_create_a_meal(self):
        old_count = Meal.objects.count()
        self.meal.save()
        new_count = Meal.objects.count()
        new_meal  = Meal.objects.first()

        self.assertNotEqual(old_count, new_count)
        self.assertEqual(new_meal.name, self.meal_name)

    def test_meal_food_association(self):
        self.meal.save()
        new_meal = Meal.objects.get(id=1)
        self.assertEqual(len(new_meal.foods.all()), 0)

        new_food = Food.objects.get(id=1)
        new_meal.foods.add(new_food)
        self.assertEqual(len(new_meal.foods.all()), 1)

        new_meal_food = new_meal.foods.get(id=1)
        self.assertEqual(new_meal_food.name, new_food.name)
        self.assertEqual(new_meal_food.calories, new_food.calories)

class MealEndpointsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.food_name = "Orange"
        self.calories = 50
        Food(name=self.food_name, calories=self.calories).save()

        self.food_name2 = "Shumai"
        self.calories2 = 350
        Food(name=self.food_name2, calories=self.calories2).save()

        self.meal_name = "Breakfast"
        Meal(name=self.meal_name).save()

        self.meal_name2 = "Lunch"
        Meal(name=self.meal_name2).save()

    def test_meal_index_endpoint(self):
        response = self.client.get('/api/v1/meals')
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['name'], self.meal_name)
        self.assertEqual(response.json()[0]['foods'], [])
        self.assertEqual(len(response.json()[0]['foods']), 0)

        self.assertEqual(response.json()[1]['name'], self.meal_name2)
        self.assertEqual(response.json()[1]['foods'], [])
        self.assertEqual(len(response.json()[1]['foods']), 0)

    def test_meal_show_endpoint(self):
        meal = Meal.objects.get(id=1)
        food = Food.objects.get(id=1)
        meal.foods.add(food)

        response = self.client.get('/api/v1/meals/1/foods')
        meal_food = response.json()['foods']
        self.assertEqual(response.json()['name'], self.meal_name)
        self.assertEqual(meal_food[0]['id'], food.id)
        self.assertEqual(meal_food[0]['name'], food.name)
        self.assertEqual(meal_food[0]['calories'], food.calories)

class MealFoodEndpointsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.food_name = "Orange"
        self.calories = 50
        Food(name=self.food_name, calories=self.calories).save()

        self.food_name2 = "Shumai"
        self.calories2 = 350
        Food(name=self.food_name2, calories=self.calories2).save()

        self.meal_name = "Breakfast"
        Meal(name=self.meal_name).save()

        self.meal_name2 = "Lunch"
        Meal(name=self.meal_name2).save()

        self.meal = Meal.objects.get(id=1)
        self.food = Food.objects.get(id=1)
        self.meal.foods.add(self.food)

    def test_meal_food_create_endpoint(self):
        response = self.client.post('/api/v1/meals/1/foods/1',{}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), f'Successfully added {self.food.name} to {self.meal.name}')
