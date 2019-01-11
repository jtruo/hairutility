from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'index.html'


class AboutUsPageView(TemplateView):
    template_name = 'about-us.html'
