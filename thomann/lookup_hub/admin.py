from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from . import models



@admin.register(models.Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = (
        "name_verbose",
        "slug",
    )


@admin.register(models.Category)
class CategoryAdmin(OrderedModelAdmin):
    list_display = (
        "name",
        "order",
        "move_up_down_links",
        "dictionary",
    )


@admin.register(models.Row)
class RowAdmin(OrderedModelAdmin):
    list_display = (
        "category",
        "order",
        "move_up_down_links",
        "is_flagged",
        "created_at",
        "updated_at",
        "en_text",
        "en_comment",
        "en_colour",
        "de_text",
        "de_comment",
        "de_colour",
        "nl_text",
        "nl_comment",
        "nl_colour",
    )
