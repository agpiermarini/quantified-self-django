# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from .serializers import FoodSerializer, MealSerializer
from .models import Food, Meal

class FoodsView(viewsets.ViewSet):

    def index(self, request):
        queryset = Food.objects.all()
        serializer = FoodSerializer(queryset, many=True)
        return Response(serializer.data)

    def show(self, request, food_id=None):
        queryset = get_object_or_404(Food, id=food_id)
        serializer = FoodSerializer(queryset, many=False)
        return Response(serializer.data)

    def create(self, request):
        queryset = Food.objects.create(name = request.data['food']['name'], calories=request.data['food']['calories'])
        serializer = FoodSerializer(queryset, many=False)
        return Response(serializer.data)

    def update(self, request, food_id):
        food = Food.objects.filter(id=food_id)
        if food.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            food.update(name = request.data['food']['name'], calories=request.data['food']['calories'])
            queryset = Food.objects.get(id=food_id)
            serializer = FoodSerializer(queryset, many=False)
            return Response(serializer.data)

    def destroy(self, request, food_id):
        get_object_or_404(Food, id=food_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MealsView(viewsets.ViewSet):

    def index(self, request):
        queryset   = Meal.objects.all()
        serializer = MealSerializer(queryset, many=True)
        return Response(serializer.data)

    def show(self, request, meal_id=None):
        queryset = get_object_or_404(Meal, id=meal_id)
        serializer = MealSerializer(queryset, many=False)
        return Response(serializer.data)

class MealFoodsView(viewsets.ViewSet):

    def create(self, request, meal_id=None, food_id=None):
        meal = get_object_or_404(Meal, id=meal_id)
        food = get_object_or_404(Food, id=food_id)
        meal.foods.add(food)
        message = f'Successfully added {food.name} to {meal.name}'
        return Response(message, status=status.HTTP_201_CREATED)

    def destroy(self, request, meal_id=None, food_id=None):
        meal = get_object_or_404(Meal, id=meal_id)
        food = get_object_or_404(Food, id=food_id)
        meal.foods.remove(food)
        message = f'Successfully removed {food.name} from {meal.name}'
        return Response(message, status=status.HTTP_202_ACCEPTED)
