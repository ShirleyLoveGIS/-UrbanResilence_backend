from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
import math
import pandas as pd
from geodetector1 import (
    factor_detector, 
    interaction_detector, 
    ecological_detector
)
from classifymethod import (
    equal_interval, 
    quantile, 
    naturalbreaks
)
# Create your views here.
from django.http import HttpResponse
from collections import defaultdict
from itertools import chain
from django.forms.models import model_to_dict


import sys
print(sys.path)

from .models import RankingList
from .models import Monthcountall
from .models import Monthcountly
from .models import RegionCount
from .models import EventsReason
from .models import MonthCountavgm
from .models import MonthCountavgy
from .models import MonthCount
from .models import Factor
from .models import OriginalEvents
from .models import RiskValue

def index(request):
    
    return render(request, 'index.html')

from django.core import serializers
import json
from django.http import JsonResponse

def merge_dict(d1, d2):
    d = defaultdict(list)

    for dd in (d1, d2):
        for key, value in d.items():
            if isinstance(value, list):
                dd[key].extend(value)
            else:
                dd[key].append(value)
    return dict(dd)

def rank_list(request):
    ranking_list = RankingList.objects.all()
    rl_str = serializers.serialize("json", ranking_list)
    rl = json.loads(rl_str)
    print(rl)   
    #[{'model': 'daping.rankinglist', 'pk': '西湖区', 'fields': {'count': 2}}, {'model': 'daping.rankinglist', 'pk': '道里区', 'fields': {'count': 1}}]
    
    return HttpResponse(json.dumps(rl), content_type='application/json')

def month_countall(request):
    monthcountall = Monthcountall.objects.all()
    rl_str = serializers.serialize("json", monthcountall)
    rl = json.loads(rl_str)
    print(rl)   
    #[{'model': 'daping.rankinglist', 'pk': '西湖区', 'fields': {'count': 2}}, {'model': 'daping.rankinglist', 'pk': '道里区', 'fields': {'count': 1}}]
    
    return HttpResponse(json.dumps(rl), content_type='application/json')

def month_countly(request):
    monthcountly = Monthcountly.objects.all()
    rl_str = serializers.serialize("json", monthcountly)
    rl = json.loads(rl_str)
    print(rl)   
    #[{'model': 'daping.rankinglist', 'pk': '西湖区', 'fields': {'count': 2}}, {'model': 'daping.rankinglist', 'pk': '道里区', 'fields': {'count': 1}}]
    
    return HttpResponse(json.dumps(rl), content_type='application/json')


def region_count(request):
    region_counting = RegionCount.objects.all()             
    rl_str = serializers.serialize("json", region_counting)
    rl = json.loads(rl_str)
    print(rl)

    return HttpResponse(json.dumps(rl), content_type='application/json')

def events_reason(request):
    events_reasoning = EventsReason.objects.all()
    rl_str = serializers.serialize("json", events_reasoning)
    rl = json.loads(rl_str)
    print(rl)

    return HttpResponse(json.dumps(rl), content_type='application/json')

def month_countavgm(request):
    month_countavgm = MonthCountavgm.objects.all()
    rl_str = serializers.serialize("json", month_countavgm)
    rl = json.loads(rl_str)
    print(rl)   

    return HttpResponse(json.dumps(rl), content_type='application/json')

def month_countavgy(request):
    month_countavgy = MonthCountavgy.objects.all()
    rl_str = serializers.serialize("json", month_countavgy)
    rl = json.loads(rl_str)
    print(rl)   

    return HttpResponse(json.dumps(rl), content_type='application/json')

def month_count(request):
    month_count = MonthCount.objects.all()
    rl_str = serializers.serialize("json", month_count)
    print(rl_str)
    rl = json.loads(rl_str)
    print(rl)
    return HttpResponse(json.dumps(rl), content_type='application/json')



def getmonth(request):
    monthcountavgm = MonthCountavgm.objects.all()
    monthcountly = Monthcountly.objects.all()
    monthcountall = Monthcountall.objects.all()
    r2_str = serializers.serialize("json", monthcountavgm)
    r2 = json.loads(r2_str)
    r3_str = serializers.serialize("json", monthcountly)
    r3 = json.loads(r3_str)
    r4_str = serializers.serialize("json", monthcountall)
    r4 = json.loads(r4_str)   
    r5 = r2+r3+r4


    return HttpResponse(json.dumps(r5), content_type='application/json')


def myview(_request):
    response = HttpResponse(json.dumps({"key": "value","key2":"value"}))
    response["Access-Control-Allow-Origin"] ="*"
    response["Access-Control-Alow-Methods"] ="POST,GET,OPTIONS"
    response["Access-Control-Max-Age"] ="1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def region_dengjiange(request):
    df = pd.DataFrame(list(Factor.objects.all().values('Y','name','roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo')))
    all_df=equal_interval(df , 5 , ['roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo'])    
    json_str = all_df.to_json(orient='records')
    json_data = json.loads(json_str)
    
    return HttpResponse(json.dumps(json_data), content_type='application/json')


def region_genweifa(request):
    df = pd.DataFrame(list(Factor.objects.all().values('Y','name','roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo')))
    all_df=quantile(df , 5 , ['roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo'])
    json_str = all_df.to_json(orient='records')
    json_data = json.loads(json_str)

    return HttpResponse(json.dumps(json_data), content_type='application/json')
 

def region_ziranfa(request):
    df = pd.DataFrame(list(Factor.objects.all().values('Y','name','roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo')))
    all_df=naturalbreaks(df , 5 , ['roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo'])
    json_str = all_df.to_json(orient='records')
    json_data = json.loads(json_str)

    return HttpResponse(json.dumps(json_data), content_type='application/json')


def factor_detec(request):
    df = pd.DataFrame(list(Factor.objects.all().values('Y','name','roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo')))
    all_df=naturalbreaks(df , 5 , ['roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo'])
    result_df=factor_detector(all_df, 'Y', ['roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo'])
    json_str = result_df.to_json(orient='records')
    json_data = json.loads(json_str)

    return HttpResponse(json.dumps(json_data), content_type='application/json')


def interaction_detec(request):
    df = pd.DataFrame(list(Factor.objects.all().values('Y','name','roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo')))
    all_df=naturalbreaks(df , 5 , ['roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo'])
    df1, df2 =interaction_detector(all_df, 'Y', ['roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo'], relationship=True)
    result_df=df1
    json_str = result_df.to_json(orient='records')
    json_data = json.loads(json_str)

    return HttpResponse(json.dumps(json_data, ensure_ascii=False), content_type='application/json')


def interaction_rela(request):
    df = pd.DataFrame(list(Factor.objects.all().values('Y','name','roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo')))
    all_df=naturalbreaks(df , 5 , ['roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo'])
    df1, df2 =interaction_detector(all_df, 'Y', ['roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo'], relationship=True)
    result_df=df2
    json_str = result_df.to_json(orient='records')
    json_data = json.loads(json_str)

    return HttpResponse(json.dumps(json_data, ensure_ascii=False), content_type='application/json')


def ecological_detec(request):
    df = pd.DataFrame(list(Factor.objects.all().values('Y','name','roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo')))
    all_df=naturalbreaks(df , 5 , ['roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo'])
    result_df=ecological_detector(all_df, 'Y', ['roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo'])
    json_str = result_df.to_json(orient='records')
    json_data = json.loads(json_str)

    return HttpResponse(json.dumps(json_data, ensure_ascii=False), content_type='application/json')

# @csrf_exempt
# def post(request):
#     data = json.loads(request.body)
#     print(data.id)
#     calriskvalue(data);


#     return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def post2(request):
    df = pd.DataFrame(list(Factor.objects.all().values('Y','name','roaddensity', 'popudensity', 'clusterdegree','elevationmean','elevationstandard','soilmiscibility','maxiareapropo')))
    data = json.loads(request.body)
    # data = [{'id': 10001, 'name': 'roaddensity', 'check': True, 'kind': 'y', 'Y': 0}, {'id': 10002, 'name': 'popudensity', 'check': True, 'kind': 'y', 'Y': 0}, {'id': 10003, 'name': 'clusterdegree', 'check': True, 'kind': 'y', 'Y': 0}, {'id': 10004, 'name': 'elevationmean', 'check': True, 'kind': 'y', 'Y': 0}, {'id': 10005, 'name': 'elevationstandard', 'check': True, 'kind': 'y', 'Y': 0}, {'id': 10006, 'name': 'soilmiscibility', 'check': True, 'kind': 'y', 'Y': 0}, {'id': 10007, 'name': 'maxiareapropo', 'check': True, 'kind': 'y', 'Y': 0}, {'id': 10008, 'name': 'Y', 'check': True, 'kind': 'x', 'Y': 0}]   
    x=[]
    for i in data:
        if(i['kind'] == 'y'):
            y=i['name']
        elif(i['kind'] == 'x'):
            x.append(i['name'])

    all_df = naturalbreaks(df , 5 , x)
    df1, df2 = interaction_detector(all_df, y, x, relationship=True)
    result_df = df1
    json_str = result_df.to_json(orient='records')
    json_data = json.loads(json_str)

    return HttpResponse(json.dumps(json_data, ensure_ascii=False), content_type='application/json')



def original_events(request):
    original_events = OriginalEvents.objects.all()
    rl_str = serializers.serialize("json", original_events)
    print(rl_str)
    rl = json.loads(rl_str)
    print(rl)
    #{"model": "daping.originalevents", "pk": 1, "fields": {"index": 1, "province": "江苏", "city": "常州", "district": "武进区", "casualty": 4, "reason": "建设工程", "link": "https://m.163.com/dy/article/E0H6T7K90521AS1H.html", "address": "武进区湖塘镇马杭东新村委郭家村一污水管网施工工地", "longitude": "119.9968", "latitude": "31.698351"}}

    return HttpResponse(json.dumps(rl), content_type='application/json')

def risk_value(request):
    risk_value = RiskValue.objects.all()
    rl_str = serializers.serialize("json", risk_value)
    print(rl_str)
    rl = json.loads(rl_str)
    print(rl)
    
    return HttpResponse(json.dumps(rl), content_type='application/json')

