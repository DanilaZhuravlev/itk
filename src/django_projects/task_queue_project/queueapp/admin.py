from django.contrib import admin
from .models import TaskQueue  # Импортируем нашу модель TaskQueue

admin.site.register(TaskQueue) # Регистрируем модель TaskQueue в Django Admin