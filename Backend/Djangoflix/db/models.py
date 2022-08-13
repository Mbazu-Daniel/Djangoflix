from django.db import models

""" This is the published state options class """


class PublishStateOptions(models.TextChoices):
    # Constant = database_value, user_display value
    PUBLISH = 'PU', "Publish"
    DRAFT = 'DR', "Draft"