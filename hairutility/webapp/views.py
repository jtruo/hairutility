from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.template.defaulttags import register
from django.http import Http404
from hairutility.users.models import HairProfile
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

    key_dict = {}

    """
    Grabs list of keys of public hair profiles from s3. Paginates the keys as well as stripping the 
    thumbnail prefix from the keys to send to the single-hair-profile view. A paginator needs to 
    be implemented for retrieval.
    """
    for key in bucket.objects.filter(Prefix='thumbnails/'):
        key_url = 'https://' + settings.AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/' + key.key
        print(key_url)
        stripped_key_url = key.key[11:]

        print(stripped_key_url)

        key_dict[key_url] = stripped_key_url

    # paginator = Paginator(key_list, 24)

    # page = request.GET.get('page')

    # keys = paginator.get_page(page)

    """Removes the empty path/object obtained from having the AWS prefix"""

    del key_dict["https://" + settings.AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/thumbnails/']

    return render(request, 'hair-profiles.html', {'key_dict': key_dict})


def single_hair_profile(request, thumbnail_key):

    hair_profile = HairProfile()

    try:
        hair_profile = HairProfile.objects.get(thumbnail_key=thumbnail_key)
    except HairProfile.DoesNotExist:
        raise Http404

    first_full_url = "https://" + settings.AWS_STORAGE_BUCKET_NAME + \
        '.s3.amazonaws.com/images/' + hair_profile.first_image_url
    # return render(request, 'hair-profiles.html')

    return render(request, 'single-hair-profile.html', {'hair_profile': hair_profile, 'first_full_url': first_full_url})


class SingleHairProfileView(TemplateView):
    template_name = 'single-hair-profile.html'
