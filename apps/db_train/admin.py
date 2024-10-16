from django.contrib import admin
from .models import Author, AuthorProfile, Tag, Entry

# Зарегистрируйте свои модели в админ панели здесь
admin.site.register([Author, AuthorProfile, Entry, Tag])

