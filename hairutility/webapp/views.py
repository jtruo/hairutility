from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import boto3

# session = boto3.Session(
#     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY

# )
# s3 = session.resource('s3')
# client = boto3.client('s3')
# bucket_name = settings.AWS_STORAGE_BUCKET_NAME

session = boto3.session.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,

)

s3 = session.resource(
    service_name='s3',
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,

)
bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)


class HomePageView(TemplateView):
    template_name = 'index.html'


class AboutUsPageView(TemplateView):
    template_name = 'about-us.html'


def hair_profiles(request):

    key_list = []

    for key in bucket.objects.filter(Prefix='images/'):
        key_urls = 'https://' + settings.AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/' + key.key
        print(key_urls)
        key_list.append(key_urls)

    paginator = Paginator(key_list, 5)

    page = request.GET.get('page')

    keys = paginator.get_page(page)

    # return render(request, 'hair-profiles.html')

    return render(request, 'hair-profiles.html', {'keys': keys})
