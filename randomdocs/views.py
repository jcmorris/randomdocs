from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import ListView
from randomdocs.models import TechDoc
from randomdocs.constants import *


class TechDocListView(ListView):
    model = TechDoc
    template_name = 'feed_display.html'


class TechDocListViewAPI(View):
    def get(self, request, *args, **kwargs):
        def serialize_tech_docs(queryset):
            return list(queryset.values('title', 'link', 'pub_date', 'category__name'))

        tech_docs = {
            'python_docs': serialize_tech_docs(TechDoc.objects.filter(category__name=PYTHON_REFERENCE, category__source__name=PYTHON).order_by('?')[:15]),
            'mdn_js_docs': serialize_tech_docs(TechDoc.objects.filter(category__name=JS_REFERENCE, category__source__name=MDN).order_by('?')[:15]),
            'mdn_http_docs': serialize_tech_docs(TechDoc.objects.filter(category__name=HTTP, category__source__name=MDN).order_by('?')[:15]),
            'mdn_web_api_docs': serialize_tech_docs(TechDoc.objects.filter(category__name=WEBAPI, category__source__name=MDN).order_by('?')[:15]),
            'vue_api_docs': serialize_tech_docs(TechDoc.objects.filter(category__name=VUE_REFERENCE, category__source__name=VUE).exclude(title='').order_by('?')[:15]),
            'wikipedia_algorithm_docs': serialize_tech_docs(TechDoc.objects.filter(category__source__name=WIKIPEDIA).order_by('?')[:15]),
            'thirty_seconds_of_code_js': serialize_tech_docs(TechDoc.objects.filter(category__source__name=THIRTY_SECONDS_OF_CODE, category__name=JS).order_by('?')[:15]),
            'thirty_seconds_of_code_python': serialize_tech_docs(TechDoc.objects.filter(category__source__name=THIRTY_SECONDS_OF_CODE, category__name=PYTHON).order_by('?')[:15]),
            'thirty_seconds_of_code_css': serialize_tech_docs(TechDoc.objects.filter(category__source__name=THIRTY_SECONDS_OF_CODE, category__name=CSS).order_by('?')[:15]),
            'django_docs': serialize_tech_docs(TechDoc.objects.filter(category__source__name=DJANGO, category__name=DJANGO_API_REFERENCE).order_by('?')[:15]),
            'typescript_docs': serialize_tech_docs(TechDoc.objects.filter(category__source__name=TYPESCRIPT, category__name=TYPESCRIPT_REFERENCE).order_by('?')[:15]),
            'postgres_docs': serialize_tech_docs(TechDoc.objects.filter(category__source__name=POSTGRESQL, category__name=POSTGRESQL_REFERENCE).order_by('?')[:15]),
            'programiz_python_docs': serialize_tech_docs(TechDoc.objects.filter(category__source__name=PROGRAMIZ, category__name=PROGRAMIZ_PYTHON_REFERENCE).order_by('?')[:15]),
            'programiz_javascript_docs': serialize_tech_docs(TechDoc.objects.filter(category__source__name=PROGRAMIZ, category__name=PROGRAMIZ_JAVSCRIPT_REFERENCE).order_by('?')[:15]),
            'css_tricks_docs': serialize_tech_docs(TechDoc.objects.filter(category__source__name=CSS_TRICKS, category__name=CSS_TRICKS_ARCHIVE).order_by('?')[:15]),
        }
        return JsonResponse(tech_docs, safe=False)
