from django.http import HttpResponse
from django.shortcuts import redirect

import json

from .detect_step_one import detect as detect_step_one
from .detect_step_two import detect as detect_step_two
 
def tooth_dectect(request):
    if request.method == 'GET':
        image_path = request.GET.get('image-path')
        conf_thres = request.GET.get('conf-thres',0.6)

        detect_results = detect_step_one(source=image_path)
        if len(detect_results) == 0:
            data = {
                'status': 'no tooth detect',
                'results': []
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

        results = detect_step_two(detect_results,conf_thres=conf_thres)

        if results:
            data = {
                'status': 'success',
                'results': results
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')
        else:
            data = {
                'status': 'fail',
                'results': []
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')