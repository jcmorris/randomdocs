from django.contrib import admin
from randomdocs.models import TechDoc, TechDocSource, TechDocCategory

@admin.register(TechDoc)
class TechDocAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'pub_date', 'category')

@admin.register(TechDocSource)
class TechDocSourceAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(TechDocCategory)
class TechDocCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'source')