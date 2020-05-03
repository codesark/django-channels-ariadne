from ariadne import load_schema_from_path
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from ..core import query

account_typedefs = load_schema_from_path("./")


@query.field("users")
@database_sync_to_async
def resolve_users(_, info):
    db_users = list(get_user_model().objects.all())
    return db_users
