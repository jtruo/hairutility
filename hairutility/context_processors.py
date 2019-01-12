import os


def export_vars(request):
    data = {}
    data['SETTING_TYPE'] = os.environ.DJANGO_SETTINGS_MODULE
    return data
