# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import FoodSerializer
from .models import Food

# Create your views here.
class FoodsView(viewsets.ViewSet):

    def index(self, request):
        queryset = Food.objects.all()
        serializer = FoodSerializer(queryset, many=True)
        return Response(serializer.data)

    def show(self, request, food_id=None):
        queryset = Food.objects.get(id=food_id)
        serializer = FoodSerializer(queryset, many=False)
        return Response(serializer.data)

    def create(self, request):
        queryset = Food.objects.create(name = request.data['name'], calories=request.data['calories'])
        serializer = FoodSerializer(queryset, many=False)
        return Response(serializer.data)

    def update(self, request, food_id):
        Food.objects.filter(id=food_id).update(name = request.data['name'], calories=request.data['calories'])
        queryset = Food.objects.get(id=food_id)
        serializer = FoodSerializer(queryset, many=False)
        return Response(serializer.data)

    def destroy(self, request, food_id):
        Food.objects.filter(id=food_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
