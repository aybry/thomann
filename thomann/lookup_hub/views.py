from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models, serialisers


class HomeView(TemplateView):
    template_name = "lookup_hub/home.html"


class DictionaryView(LoginRequiredMixin, TemplateView):
    template_name = "lookup_hub/dictionary.html"

    def get_context_data(self, slug, **kwargs):
        dictionary = models.Dictionary.objects.get(slug=slug)
        dictionary_srl = serialisers.DictionarySerialiser(dictionary)

        return {
            "dictionary": dictionary,
            "dictionary_data": dictionary_srl.data,
        }


class SandboxView(DictionaryView):
    def get_context_data(self, **kwargs):
        sandbox_dictionary = models.Dictionary.objects.get(slug="sandbox")
        dictionary_srl = serialisers.DictionarySerialiser(sandbox_dictionary)

        return {
            "dictionary": sandbox_dictionary,
            "dictionary_data": dictionary_srl.data,
        }


class GuideView(TemplateView):
    template_name = "lookup_hub/guide.html"
