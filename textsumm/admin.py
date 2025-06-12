from django.contrib import admin
from .models import TextSumm


class TextsummAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'image', 'video', 'lineage', 'conversion', 'persecution', 'hijrah', 'battle', 'trait', 'death')

admin.site.register(TextSumm, TextsummAdmin)
