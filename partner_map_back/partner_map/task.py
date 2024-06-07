import requests
from .models import Bonus
from celery import shared_task
from crontab import CronTab
import logging

logger = logging.getLogger(__name__)


def sync_bonuses():
    url = 'https://dev-bls-api.oemgroup.ru/api/reference/bonuses?search=&page=1&per_page=20'

    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmVzX2luIjoiMTk3MC0wMS0wMVQwMDowMDowMFoiLCJzZXJ2aWNlX25hbWUiOiJkZXYifQ.B9rcaIWWdlh2-CLekjjRAytkkOWNidJX1u0EjRgt-ZU'
    }
    params = {
        "search": "",
        "page": 1,
        "per_page": 20
    }

    response = requests.get(url, headers=headers, params=params)

    logger.info(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        bonuses = response.json().get('items', [])  # предполагается, что данные в ключе 'data'
        logger.info(f"Bonuses data: {bonuses}")
        for bonus_data in bonuses:
            Bonus.objects.update_or_create(
                name=bonus_data['name'],
                defaults={
                    'id_bonus': bonus_data['id'],
                    'image': bonus_data['image']
                }
            )
    else:
        logger.error(f"Failed to fetch bonuses: {response.status_code}")
