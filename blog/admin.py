from django.contrib import admin
from .models import Article


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'create_date')

    list_filter = ('status',)

    list_per_page = 10


admin.site.register(Article, ArticleAdmin)
