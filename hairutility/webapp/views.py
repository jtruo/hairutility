from django.views.generic import TemplateView, ListView
from django.template import Context
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.template.defaulttags import register
from django.http import Http404
from django.utils.decorators import method_decorator
from hairutility.users.models import HairProfile

from hairutility.decorators import BasicAuthDecorator
import boto3


session = boto3.session.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,

)

s3 = session.resource(
    service_name='s3',
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,

)

s3Client = boto3.client('s3', region_name='us-east-2')

bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)


@method_decorator(BasicAuthDecorator, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'index.html'

    key_dict = {}
    hair_profiles = HairProfile.objects.order_by("-created")[:8]

    for hair_profile in hair_profiles:

        thumbnail_key = hair_profile.thumbnail_key

        full_key_url = 'https://' + settings.AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/thumbnails/' + thumbnail_key

        key_dict[full_key_url] = thumbnail_key

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        context['key_dict'] = self.key_dict
        context['hair_profiles'] = self.hair_profiles
        return context


@method_decorator(BasicAuthDecorator, name='dispatch')
class AboutUsPageView(TemplateView):
    template_name = 'about-us.html'


@method_decorator(BasicAuthDecorator, name='dispatch')
class HairProfilesView(TemplateView):
    template_name = 'hair-profiles.html'

    key_dict = {}
    hair_profiles = HairProfile.objects.order_by("-created")

    for hair_profile in hair_profiles:

        thumbnail_key = hair_profile.thumbnail_key

        full_key_url = 'https://' + settings.AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/thumbnails/' + thumbnail_key

        key_dict[full_key_url] = thumbnail_key

# Need a paginator in the future

    def get_context_data(self, *args, **kwargs):
        context = super(HairProfilesView, self).get_context_data(*args, **kwargs)
        context['key_dict'] = self.key_dict
        context['hair_profiles'] = self.hair_profiles
        return context


# @BasicAuthDecoratorr
def single_hair_profile(request, thumbnail_key=''):

    hair_profile = HairProfile()

    if not thumbnail_key:
        return redirect('single-hair-profile')

    else:
        try:
            hair_profile = HairProfile.objects.get(thumbnail_key=thumbnail_key)
        except HairProfile.DoesNotExist:
            raise Http404

        full_url_prefix = "https://" + settings.AWS_STORAGE_BUCKET_NAME + \
            '.s3.amazonaws.com/images/'

        first_image_key = full_url_prefix + hair_profile.first_image_key
        second_image_url = full_url_prefix + hair_profile.second_image_url
        third_image_url = full_url_prefix + hair_profile.third_image_url
        fourth_image_url = full_url_prefix + hair_profile.fourth_image_url

        return render(request, 'single-hair-profile.html',
                      {'hair_profile': hair_profile,
                       'first_image_key': first_image_key,
                       'second_image_url': second_image_url,
                       'third_image_url': third_image_url,
                       'fourth_image_url': fourth_image_url})


# class SingleHairProfileView(TemplateView):

#     template_name = 'single-hair-profile.html'

#     hair_profile = HairProfile()
#     first_image_key = ""
#     second_image_url = ""
#     third_image_url = ""
#     fourth_image_url = ""


#     print(thumbnail_key)

#     if not thumbnail_key:
#         print("Thumbnail_key is missing")

#     else:
#         try:
#             hair_profile = HairProfile.objects.get(thumbnail_key=thumbnail_key)
#         except HairProfile.DoesNotExist:
#             raise Http404

#         full_url_prefix = "https://" + settings.AWS_STORAGE_BUCKET_NAME + \
#             '.s3.amazonaws.com/images/'

#         first_image_key = full_url_prefix + hair_profile.first_image_k
#         second_image_url = full_url_prefix + hair_profile.second_image_url
#         third_image_url = full_url_prefix + hair_profile.third_image_url
#         fourth_image_url = full_url_prefix + hair_profile.fourth_image_url

#     def get_context_data(self, *args, **kwargs):
#         context = super(SingleHairProfileView, self).get_context_data(*args, **kwargs)
#         context['hair_profile'] = self.hair_profile
#         context['first_image_key'] = self.first_image_k
#         context['second_image_url'] = self.second_image_url
#         context['third_image_url'] = self.third_image_url
#         context['fourth_image_url'] = self.fourth_image_url

#         return context

@method_decorator(BasicAuthDecorator, name='dispatch')
class FAQView(TemplateView):
    template_name = 'faq.html'


@method_decorator(BasicAuthDecorator, name='dispatch')
class WorkInProgressView(TemplateView):
    template_name = 'wip.html'
