from django import template
register = template.Library()
from Home.models import API_Device_data

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