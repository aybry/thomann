import uuid

from django.db import models
from ordered_model.models import OrderedModel


class Dictionary(models.Model):
    slug = models.CharField(max_length=50, unique=True)
    name_verbose = models.CharField(max_length=200, default="")

    class Meta:
        verbose_name_plural = "Dictionaries"

    def __str__(self):
        return f"<Dictionary {self.slug}>"


class Category(OrderedModel):
    GROUP_NAME = "cat"

    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    dictionary = models.ForeignKey(Dictionary, null=True, default=None, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("order",)

    def __str__(self):
        return f"<Category {self.name}>"


class Row(OrderedModel):
    GROUP_NAME = "row"

    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    ordered_with_respect_to = "category"

    is_flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    en_text = models.CharField(max_length=500, blank=True, default="")
    en_comment = models.CharField(max_length=2000, blank=True, default="")
    en_colour = models.CharField(max_length=6, blank=True, default="")

    de_text = models.CharField(max_length=500, blank=True, default="")
    de_comment = models.CharField(max_length=2000, blank=True, default="")
    de_colour = models.CharField(max_length=6, blank=True, default="")

    nl_text = models.CharField(max_length=500, blank=True, default="")
    nl_comment = models.CharField(max_length=2000, blank=True, default="")
    nl_colour = models.CharField(max_length=6, blank=True, default="")

    class Meta:
        ordering = ("order",)