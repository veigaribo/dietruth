import uuid
from django.db import models


class Roll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=280, blank=True)

    # "1d20", "6d6", "1d20+2"
    query = models.CharField(max_length=60)

    # "18", "6;2;3;5;3;3", "1"
    result = models.CharField(max_length=500)

    # "0", "0", "2"
    modifier = models.IntegerField(default=0)

    # if using a random.org license that allows it
    # will be a SHA-512 hash in base64
    signature = models.CharField(max_length=684, null=True)

    # will store the `random` field of the random.org response
    # necessary to check against the signature
    randomdata = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
