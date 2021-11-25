from django.http import HttpResponse
from django.shortcuts import redirect

import json

from .detect_step_one import detect as detect_step_one
from .detect_step_two import detect as detect_step_two
 
def hello(request):
    if request.method == 'GET':
        image_path = request.GET.get('image-path')
        print(image_path)

        detect_results = detect_step_one(source=image_path)
        results = detect_step_two(detect_results)
        json_obj = json.dumps(results, ensure_ascii=False)

        return HttpResponse(json_obj)