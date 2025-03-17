from django.test import TestCase
from .models import TaskQueue
from .fetcher import fetch_task

class FetchTaskTest(TestCase):

    def test_fetch_single_task(self):
        """
        Тест проверяет, что fetch_task() корректно извлекает одну задачу
        со статусом 'pending' и меняет ее статус на 'in_progress'.
        """
        task1 = TaskQueue.objects.create(task_name="Test Task 1", status='pending')
        fetched_task = fetch_task()

        self.assertIsNotNone(fetched_task, "fetch_task() должен вернуть задачу, а не None")
        self.assertEqual(fetched_task.status, 'in_progress', "Статус извлеченной задачи должен быть 'in_progress'")
        updated_task_from_db = TaskQueue.objects.get(pk=task1.pk)
        self.assertEqual(updated_task_from_db.status, 'in_progress', "Статус задачи в базе данных должен быть 'in_progress'")