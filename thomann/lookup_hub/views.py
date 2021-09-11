import logging
import json
from datetime import datetime

from django.http import Http404
from django.http import JsonResponse
from django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.management import call_command

from . import models, serialisers


LOGGER = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = "lookup_hub/home.html"


class DictionaryView(LoginRequiredMixin, TemplateView):
    template_name = "lookup_hub/dictionary.html"

    def get_context_data(self, slug, **_):
        dictionary = models.Dictionary.objects.get(slug=slug)
        dictionary_barebones_srl = serialisers.DictionaryBarebonesSerialiser(dictionary)

        return {
            "dictionary": dictionary_barebones_srl.data,
            "show_socket_button": True,
            "show_backup_button": True,
        }


class DictionaryDataView(LoginRequiredMixin, View):

    def get(self, _request, slug, **_):
        dictionary = models.Dictionary.objects.get(slug=slug)
        dictionary_srl = serialisers.DictionarySerialiser(dictionary)

        return JsonResponse(dictionary_srl.data)


class SandboxView(TemplateView):
    template_name = "lookup_hub/dictionary.html"

    def get_context_data(self, **_):
        sandbox_dictionary = models.Dictionary.objects.get(slug="sandbox")
        sandbox_barebones_srl = serialisers.DictionaryBarebonesSerialiser(sandbox_dictionary)

        return {
            "dictionary": sandbox_barebones_srl.data,
            "show_socket_button": True,
        }


class SandboxDataView(View):

    def get(self, _request, **_):
        dictionary = models.Dictionary.objects.get(slug="sandbox")
        dictionary_srl = serialisers.DictionarySerialiser(dictionary)

        return JsonResponse(dictionary_srl.data)


class GetBackupView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return Http404

        backup_filename = f"backups/{datetime.now().isoformat()}.json"
        LOGGER.info(f"Saving backup to: {backup_filename}")

        with open(backup_filename, "w") as output_f:
            call_command("dumpdata", "lookup_hub", stdout=output_f)

        with open(backup_filename, "r") as input_f:
            db_data_all = json.loads(input_f.read())

        return JsonResponse(db_data_all, safe=False)


class GuideView(TemplateView):
    template_name = "lookup_hub/guide.html"
