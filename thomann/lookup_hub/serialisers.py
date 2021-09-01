from rest_framework import serializers

from . import models


class RowSerialiser(serializers.ModelSerializer):

    class Meta:
        model = models.Row
        fields = (
            "id",
            "category",
            "deleted_from",
            "is_deleted",
            "is_flagged",
            "created_at",
            "updated_at",
            "deleted_at",
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



class DeletedRowSerialiser(serializers.ModelSerializer):
    category_name = serializers.CharField(source="deleted_from.name", read_only=True)

    class Meta:
        model = models.Row
        fields = (
            "id",
            "category_name",
            "deleted_at",
            "en_text",
            "de_text",
            "nl_text",
        )


class CategorySerialiser(serializers.ModelSerializer):
    row_set = RowSerialiser(many=True)

    class Meta:
        model = models.Category
        fields = (
            "id",
            "name",
            "dictionary",
            "row_set",
        )


class CategoryBarebonesSerialiser(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = (
            "id",
            "name",
            "dictionary",
        )


class DictionarySerialiser(serializers.ModelSerializer):
    category_set = CategorySerialiser(many=True)

    class Meta:
        model = models.Dictionary
        fields = (
            "slug",
            "name_verbose",
            "category_set",
        )


class DictionaryBarebonesSerialiser(serializers.ModelSerializer):

    class Meta:
        model = models.Dictionary
        fields = (
            "slug",
            "name_verbose",
        )
