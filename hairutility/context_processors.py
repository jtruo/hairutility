import os


def export_vars(request):
    data = {}
    data['S3_PREFIX'] = os.environ.DJANGO_SETTINGS_MODULE
    return data
