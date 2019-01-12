import os


def export_vars(request):
    data = {}
    data['S3_PREFIX'] = os.environ.S3_PREFIX
    return data
