from django.db.models import Sum
from django.db.models import FloatField
from django.db.models.functions import Cast
from django import template
register = template.Library()
from Home.models import API_Device_data


# method

def inp(data, data2):
  data = API_Device_data.objects.filter(hours=data2, date=data).annotate(as_float=Cast('count_input', FloatField())).aggregate(Sum('as_float'))['as_float__sum']
  try:
    data = round(data)
  except Exception as e:
    print(e)
    data = 0
  return data

def output(data, data2):
  data = API_Device_data.objects.filter(hours=data2, date=data).annotate(as_float=Cast('count_output', FloatField())).aggregate(Sum('as_float'))['as_float__sum']
  try:
    data = round(data)
  except Exception as e:
    print(e)
    data = 0
  return data

@register.filter(name='scrapeds')
def scrapeds(pk):
  obj = API_Device_data.objects.get(pk=pk)
  data =  int(obj.count_input) - int(obj.count_output)
  return data

@register.filter(name='get_availability')
def get_availability(get_availability):
  return get_availability['y']

@register.filter(name='get_performance')
def get_performance(get_performance):
  return get_performance['y']

@register.filter(name='get_get_quality')
def get_get_quality(get_get_quality):
  return get_get_quality['y']

@register.filter(name='get_oee')
def get_oee(get_oee):
  return get_oee['y']

@register.filter(name='mix_data')
def mix_data(mix_data):
  return mix_data['y']

@register.filter(name='get_count')
def get_count(data, data2):
  a = API_Device_data.objects.filter(hours=data, state__icontains=data2).count()
  return a


@register.filter(name='produce_unit')
def produce_unit(data, data2):
  _inp = inp(data, data2)
  return _inp


@register.filter(name='scraped_unit')
def scraped_unit(data, data2):
  _inp = inp(data, data2)
  _out = output(data, data2)
  return _inp - _out