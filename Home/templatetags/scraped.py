from django.db.models import Sum
from django.db.models import FloatField
from django.db.models.functions import Cast
from django import template
register = template.Library()
from Home.models import API_Device_data, Devices


# method

def inp(data, data2):
  print(f"Data {data} Data2 {data2}")
  # my_device = Devices.objects.get(device_id=device_id)
  data = API_Device_data.objects.filter(
     hours=data2, date=data
    ).annotate(as_float=Cast('count_input', FloatField())).aggregate(Sum('as_float'))['as_float__sum']
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


def rat(sec, data, data2):

  iot_data = API_Device_data.objects.filter(hours=data, date=data2)

  total_state = 0
  total_state_production = 0
  total_state_off = 0
  total_output = 0
  total_cadence = 0

  _availability = 0
  _quality = 0
  _performance = 0
  _oee = 0
  for obj in iot_data:
    total_state += 1
    if obj.state and obj.state.upper() == "PRODUCTION":
        total_state_production += 1
    if obj.state and obj.state.upper()  == "OFF":
        total_state_off += 1

    if obj.count_output and obj.count_output:
        total_output += float(obj.count_output)
    if obj.cadence and obj.state.upper() == 'PRODUCTION':
        try:
            total_cadence += float(obj.cadence)
        except Exception as e:
            total_cadence += float(1)
    


    # Availability rate
    try:
        calculation_data = (
            (total_state - total_state_off - total_state_production) / (total_state - total_state_off)
        )
        calculation = round(calculation_data)
    except Exception as e:
        calculation = 0
        calculation_data = 0
    _availability += calculation

    # Quality rate
    _input = obj.count_input
    _output = obj.count_output
    try:
        i_o_data = (float(_output) / float(_input))
        i_o = (round(i_o_data))
    except Exception as e:
        i_o = float(100)
        i_o_data = float(1)
    _quality += round(i_o)
    

    # Performance rate
    try:
        performance_data = (total_output / total_cadence)
        performance = round(performance_data)
    except Exception as e:
        performance = float(1)
        performance_data = float(1)
    _performance += round(performance)



    # OEE
    data = (calculation_data * i_o_data * performance_data)
    _oee += round(data)


    # State occurrences Stop
    # if obj.state and obj.state.title() == "Stop" and obj.stop and obj.stop.title() not in stop_label_list:
    #     stop_label_list.append(obj.stop.title())

    # # State occurrences Breakdown
    # if obj.state and obj.state.title() == "Breakdown" and obj.stop and obj.stop.title() not in breakdown_label_list:
    #     breakdown_label_list.append(obj.stop.title())
  try:
     _quality = round(_quality / iot_data.count())
  except Exception as e:
     print(e)
  if sec == "ava":
    return _availability
  if sec == "qua":
    return _quality
  if sec == "per":
    return _performance
  if sec == "oee":
    return _oee



@register.filter(name='scrapeds')
def scrapeds(pk):
  obj = API_Device_data.objects.get(pk=pk)
  data =  int(obj.count_input) - int(obj.count_output)
  return data


@register.filter(name='get_availability')
def get_availability(data2, data):
  sec = "ava"
  _availability = rat(sec, data, data2)
  return _availability

@register.filter(name='get_performance')
def get_performance(data2, data):
  sec = "per"
  _availability = rat(sec, data, data2)
  return _availability

@register.filter(name='get_quality')
def get_quality(data2, data):
  sec = "qua"
  _availability = rat(sec, data, data2)
  return _availability

@register.filter(name='get_oee')
def get_oee(data2, data):
  sec = "oee"
  oee = rat(sec, data, data2)
  return oee




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