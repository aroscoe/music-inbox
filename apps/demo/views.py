from django.views.generic.simple import direct_to_template

def upload(request):
    return direct_to_template(request, 'demo/upload.html', locals())