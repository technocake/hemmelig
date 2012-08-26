from django.template.response import TemplateResponse


def index(req):
    return TemplateResponse(req, 'map/index.html')
