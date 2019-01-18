from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import boto3

session = boto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY

)
s3 = session.resource('s3')
client = boto3.client('s3')
my_bucket = s3.Bucket('hairutility-prod')


class HomePageView(TemplateView):
    template_name = 'index.html'


class AboutUsPageView(TemplateView):
    template_name = 'about-us.html'


def hair_profiles(request):

    key_list = []

    for key in my_bucket.objects.filter(Prefix='images/'):
        key_urls = 'https://s3.us-east-2.amazonaws.com/hairutility-prod/' + key.key
        print(key_urls)
        key_list.append(key_urls)

    paginator = Paginator(key_list, 5)

    page = request.GET.get('page')

    keys = paginator.get_page(page)

    # return render(request, 'hair-profiles.html')

    return render(request, 'hair-profiles.html', {'keys': keys})
