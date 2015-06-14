from rest_framework.renderers import JSONRenderer as DRFJSONRenderer

class JSONRenderer(DRFJSONRenderer):
    charset = 'utf-8'
