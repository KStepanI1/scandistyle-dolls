from typing import List

from asgiref.sync import sync_to_async

from django_project.usersmanage.models import Item


@sync_to_async
def add_item(**kwargs):
    return Item(**kwargs).save()


@sync_to_async
def get_items() -> List[Item]:
    return Item.objects.all()


@sync_to_async
def get_item(item_id) -> Item:
    return Item.objects.filter(id=int(item_id)).first()
