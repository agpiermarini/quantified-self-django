# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Food(models.Model):
    name       = models.CharField(max_length=100, blank=False)
    calories   = models.PositiveIntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)

class Meal(models.Model):
    name       = models.CharField(max_length=100, blank=False)
    foods      = models.ManyToManyField(Food)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
