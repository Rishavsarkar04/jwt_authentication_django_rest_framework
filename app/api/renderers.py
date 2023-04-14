from rest_framework import renderers
import json

class MyUserRenderers(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # print(f'{str(data)} and in first')
        response = ''
        if 'ErrorDetails' in str(data):
            # print(f'{data} and in if')
            response = json.dumps({'error':data})
        else:
            # print(f'{data} and in else')
            response = json.dumps(data)
        return response