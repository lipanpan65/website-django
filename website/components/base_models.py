import datetime
from django.db import models

"""
non_db_attrs = (
    "blank",
    "choices",
    "db_column",
    "editable",
    "error_messages",
    "help_text",
    "limit_choices_to",
    # Database-level options are not supported, see #21961.
    "on_delete",
    "related_name",
    "related_query_name",
    "validators",
    "verbose_name",
)

"""


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=datetime.datetime.now())
    update_time = models.DateTimeField(auto_now_add=datetime.datetime.now())

    class Meta:
        abstract = True
        # ordering = ["-create_time", "-update_time"]
