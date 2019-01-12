import os
from django.conf import settings


def export_vars(request):
    data = {}
    data['S3_PREFIX'] = settings.S3_PREFIX
    print(data)
    return data
