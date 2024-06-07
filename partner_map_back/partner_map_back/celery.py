# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
# from celery.schedules import crontab
#
# # Устанавливаем переменную окружения для настройки Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'partner_map_back.settings')
#
# # Создаем экземпляр приложения Celery
# app = Celery('partner_map_back')
#
# # Загружаем конфигурацию из настроек Django
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Автоматически обнаруживаем задачи (tasks) в каждом приложении
# app.autodiscover_tasks()
#
#
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
#
#
# app.conf.beat_schedule = {
#     'sync-bonuses-every-hour': {
#         'task': 'partner_map.tasks.sync_bonuses',
#         'schedule': crontab(minute=0, hour='*/1'),  # каждые 1 час
#     },
# }
#
# app.conf.timezone = 'UTC'
