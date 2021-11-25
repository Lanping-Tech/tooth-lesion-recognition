from django.http import HttpResponse
from django.shortcuts import redirect

import json
 
def hello(request):
    if request.method == 'GET':
        image_path = request.GET.get('image-path')
        
        result = {}
        json_obj = json.dumps(result, ensure_ascii=False)

        return HttpResponse(json_obj)