from asgiref.sync import sync_to_async

from django_project.usersmanage.models import Document


@sync_to_async
def add_document(name, file_id):
    try:
        Document(name=name, file_id=file_id)
    except Exception as err:
        pass
