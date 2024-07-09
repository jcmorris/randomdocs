from django.core.management.base import BaseCommand

from randomdocs.constants import *
from randomdocs.models import TechDocSource, TechDocCategory, TechDoc
from randomdocs.scrape_utils import *


class Command(BaseCommand):
    help = 'Scrape technical documentation from various sources.'

    def handle(self, *args, **kwargs):
        # self.scrape_mdn_webapi()
        # self.scrape_mdn_js_reference()
        # self.scrape_mdn_http_reference()
        # self.scrape_vue_docs()
        # self.scrape_python_docs()
        # self.scrape_wikipedia_articles()
        # self.scrape_30_seconds_of_code_js_docs()
        # self.scrape_30_seconds_of_code_python_docs()
        # self.scrape_30_seconds_of_code_css_docs()
        # self.scrape_django_api_docs()
        # self.scrape_typescript_docs()
        # self.scrape_postgresql_docs()
        self.scrape_programiz_python_docs()
        # self.scrape_programiz_javascript_docs()
        # self.scrape_css_tricks_archive()

    def create_articles(self, category, articles):
        for article in articles:
            TechDoc.objects.get_or_create(
                title=article['title'],
                link=article['url'],
                category=category
            )

    def scrape_mdn_webapi(self):
        articles = get_mdn_webapi_links()
        source, _ = TechDocSource.objects.get_or_create(name=MDN)
        category, _ = TechDocCategory.objects.get_or_create(name=WEBAPI, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} MDN {WEBAPI} docs scraped successfully!")

    def scrape_mdn_js_reference(self):
        articles = get_mdn_js_reference_links()
        source, _ = TechDocSource.objects.get_or_create(name=MDN)
        category, _ = TechDocCategory.objects.get_or_create(name=JS_REFERENCE, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} MDN {JS_REFERENCE} docs scraped successfully!")

    def scrape_mdn_http_reference(self):
        articles = get_mdn_http_reference_links()
        source, _ = TechDocSource.objects.get_or_create(name=MDN)
        category, _ = TechDocCategory.objects.get_or_create(name=HTTP, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} MDN {HTTP} docs scraped successfully!")

    def scrape_vue_docs(self):
        articles = get_vue_links()
        source, _ = TechDocSource.objects.get_or_create(name=VUE)
        category, _ = TechDocCategory.objects.get_or_create(name=VUE_REFERENCE, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} {VUE} docs scraped successfully!")

    def scrape_python_docs(self):
        articles = get_python_links()
        source, _ = TechDocSource.objects.get_or_create(name=PYTHON)
        category, _ = TechDocCategory.objects.get_or_create(name=PYTHON_REFERENCE, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} {PYTHON} docs scraped successfully!")

    def scrape_wikipedia_articles(self):
        categories = [COMPUTER_SCIENCE, PROGRAMMING_LANGUAGES]
        articles = get_links_from_wikipedia_categories(categories)
        source, _ = TechDocSource.objects.get_or_create(name=WIKIPEDIA)
        for article in articles:
            category_name = article['title'].split(':')[0] if ':' in article['title'] else "General"
            category, _ = TechDocCategory.objects.get_or_create(name=category_name, source=source)
            TechDoc.objects.get_or_create(
                title=article['title'],
                link=article['url'],
                category=category
            )
        print(f"{len(articles)} Wikipedia articles scraped successfully!")

    def scrape_30_seconds_of_code_js_docs(self):
        articles = get_30_seconds_of_code_links(JS)
        source, _ = TechDocSource.objects.get_or_create(name=THIRTY_SECONDS_OF_CODE)
        category, _ = TechDocCategory.objects.get_or_create(name=JS, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} {THIRTY_SECONDS_OF_CODE} {JS} docs scraped successfully!")

    def scrape_30_seconds_of_code_python_docs(self):
        articles = get_30_seconds_of_code_links(PYTHON)
        source, _ = TechDocSource.objects.get_or_create(name=THIRTY_SECONDS_OF_CODE)
        category, _ = TechDocCategory.objects.get_or_create(name=PYTHON, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} {THIRTY_SECONDS_OF_CODE} {PYTHON} docs scraped successfully!")

    def scrape_30_seconds_of_code_css_docs(self):
        articles = get_30_seconds_of_code_links(CSS)
        source, _ = TechDocSource.objects.get_or_create(name=THIRTY_SECONDS_OF_CODE)
        category, _ = TechDocCategory.objects.get_or_create(name=CSS, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} {THIRTY_SECONDS_OF_CODE} {CSS} docs scraped successfully!")

    def scrape_django_api_docs(self):
        articles = get_django_usage_links()
        source, _ = TechDocSource.objects.get_or_create(name=DJANGO)
        category, _ = TechDocCategory.objects.get_or_create(name=DJANGO_API_REFERENCE, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} {DJANGO_API_REFERENCE} docs scraped successfully!")

    def scrape_typescript_docs(self):
        articles = scrape_typescript_docs()
        source, _ = TechDocSource.objects.get_or_create(name=TYPESCRIPT)
        category, _ = TechDocCategory.objects.get_or_create(name=TYPESCRIPT_REFERENCE, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} {TYPESCRIPT_REFERENCE} docs scraped successfully!")

    def scrape_postgresql_docs(self):
        articles = scrape_postgresql_docs()
        source, _ = TechDocSource.objects.get_or_create(name=POSTGRESQL)
        category, _ = TechDocCategory.objects.get_or_create(name=POSTGRESQL_REFERENCE, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} {POSTGRESQL_REFERENCE} docs scraped successfully!")

    def scrape_programiz_python_docs(self):
        articles = scrape_programiz_python()
        source, _ = TechDocSource.objects.get_or_create(name=PROGRAMIZ)
        category, _ = TechDocCategory.objects.get_or_create(name=PROGRAMIZ_PYTHON_REFERENCE, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} {PROGRAMIZ_PYTHON_REFERENCE} docs scraped successfully!")

    def scrape_programiz_javascript_docs(self):
        articles = scrape_programiz_javascript()
        source, _ = TechDocSource.objects.get_or_create(name=PROGRAMIZ)
        category, _ = TechDocCategory.objects.get_or_create(name=PROGRAMIZ_JAVSCRIPT_REFERENCE, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} {PROGRAMIZ_JAVSCRIPT_REFERENCE} docs scraped successfully!")

    def scrape_css_tricks_archive(self):
        articles = scrape_css_tricks_archives()
        source, _ = TechDocSource.objects.get_or_create(name=CSS_TRICKS)
        category, _ = TechDocCategory.objects.get_or_create(name=CSS_TRICKS_ARCHIVE, source=source)
        self.create_articles(category, articles)
        print(f"{len(articles)} {CSS_TRICKS_ARCHIVE} docs scraped successfully!")
