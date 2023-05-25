from django.db.models import Sum
from django.db.models import FloatField
from django.db.models.functions import Cast
from django import template
register = template.Library()
from Home.models import API_Device_data, Devices


# method

def inp(date, data2):
  try:
    my_device = Devices.objects.get(device_id=date[1])
    data = API_Device_data.objects.filter(
      serial_no=my_device.serial_no,
      device_password=my_device.device_password,
      hours=data2, date=date[0], 
      ).annotate(as_float=Cast('count_input', FloatField())).aggregate(Sum('as_float'))['as_float__sum']
    try:
      data = round(data)
    except Exception as e:
      data = 0
    return data
  except Devices.DoesNotExist:
     return 0

def date_inp(data):
  # my_device = Devices.objects.get(device_id=device_id)
  data = API_Device_data.objects.filter(
     date=data
    ).annotate(as_float=Cast('count_input', FloatField())).aggregate(Sum('as_float'))['as_float__sum']
  try:
    data = round(data)
  except Exception as e:
    data = 0
  return data

def output(date, data2):
  my_device = Devices.objects.get(device_id=date[1])
  data = API_Device_data.objects.filter(
    serial_no=my_device.serial_no,
    device_password=my_device.device_password,
    hours=data2, date=date[0], 
  ).annotate(as_float=Cast('count_output', FloatField())).aggregate(Sum('as_float'))['as_float__sum']
  try:
    data = round(data)
  except Exception as e:
    data = 0
  return data


def date_output(data):
  data = API_Device_data.objects.filter(date=data).annotate(as_float=Cast('count_output', FloatField())).aggregate(Sum('as_float'))['as_float__sum']
  try:
    data = round(data)
  except Exception as e:
    data = 0
  return data



def date_data(data, val):
  data = API_Device_data.objects.filter(date=data).annotate(as_float=Cast(val, FloatField())).aggregate(Sum('as_float'))['as_float__sum']
  try:
    data = round(data)
  except Exception as e:
    data = 0
  return data


def rat(sec, data, data2):
  my_device = Devices.objects.get(device_id=data2[1])
  iot_data = API_Device_data.objects.filter(
     hours=data, date=data2[0], serial_no=my_device.serial_no,
    device_password=my_device.device_password,
    )

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
     _quality = 0
  if sec == "ava":
    return _availability
  if sec == "qua":
    return _quality
  if sec == "per":
    return _performance
  if sec == "oee":
    return _oee


def date_rat(sec, data):

  iot_data = API_Device_data.objects.filter(date=data)

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


  try:
     _quality = round(_quality / iot_data.count())
  except Exception as e:
     _quality = 0
  try:
     _availability = round(_availability / iot_data.count())
  except Exception as e:
     _availability = 0
  try:
     _performance = round(_performance / iot_data.count())
  except Exception as e:
     _performance = 0
  try:
     _oee = round(_oee / iot_data.count())
  except Exception as e:
     _oee = 0
  if sec == "ava":
    return _availability
  if sec == "qua":
    return _quality
  if sec == "per":
    return _performance
  if sec == "oee":
    return _oee



def hours(data, data2, state):
   my_device = Devices.objects.get(device_id=data[1])

   iot_data = API_Device_data.objects.filter(
      hours=data2, date=data[0], state__icontains=state,
      serial_no=my_device.serial_no, device_password=my_device.device_password,
    ).count()
   return iot_data


def date_hours(data, state):
   iot_data = API_Device_data.objects.filter(
      date=data, state__icontains=state
    ).count()
   return iot_data


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




@register.filter(name='get_breakdown')
def get_breakdown(data, data2):
  brek = hours(data, data2, state="Breakdown")
  return brek

@register.filter(name='get_unknown')
def get_unknown(data, data2):
  brek = hours(data, data2, state="Unknown")
  return brek

@register.filter(name='get_off')
def get_off(data, data2):
  brek = hours(data, data2, state="Off")
  return brek

@register.filter(name='get_stop')
def get_stop(data, data2):
  brek = hours(data, data2, state="Stop")
  return brek

@register.filter(name='get_production')
def get_production(data, data2):
  brek = hours(data, data2, state="Production")
  return brek

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


# Date ========================================================================

@register.filter(name='date_product')
def date_product(data):
  _inp = date_inp(data)
  return _inp

@register.filter(name='date_scraped')
def date_scraped(data):
  _inp = date_inp(data)
  _out = date_output(data)
  return _inp - _out

@register.filter(name='date_availability')
def date_availability(data):
  sec = "ava"
  _availability = date_rat(sec, data)
  return _availability

@register.filter(name='date_performance')
def date_performance(data):
  sec = "per"
  _availability = date_rat(sec, data)
  return _availability

@register.filter(name='date_quality')
def date_quality(data):
  sec = "qua"
  _availability = date_rat(sec, data)
  return _availability

@register.filter(name='date_oee')
def date_oee(data):
  sec = "oee"
  oee = date_rat(sec, data)
  return oee


@register.filter(name='date_breakdown')
def date_breakdown(data):
  brek = date_hours(data, state="Breakdown")
  return brek

@register.filter(name='date_unknown')
def date_unknown(data):
  brek = date_hours(data, state="Unknown")
  return brek

@register.filter(name='date_off')
def date_off(data):
  brek = date_hours(data, state="Off")
  return brek

@register.filter(name='date_stop')
def date_stop(data):
  brek = date_hours(data, state="Stop")
  return brek

@register.filter(name='date_production')
def date_production(data):
  brek = date_hours(data, state="Production")
  return brek

@register.filter(name='date_mtbf')
def date_mtbf(data):
  qs = API_Device_data.objects.filter(date=data)
  all_state = qs.exclude(state__icontains="Off").count()
  all_mtbf = qs.filter(mtbf__icontains="1").count()
  try:
      summary = all_state / all_mtbf
  except Exception as e:
      summary = 0
  return summary

@register.filter(name='date_mttr')
def date_mttr(data):
  qs = API_Device_data.objects.filter(date=data)
  all_mtbf = qs.filter(mtbf__icontains="1").count()
  all_mttr = qs.filter(mttr__icontains="1").count()
  try:
      summary = all_mttr / all_mtbf
  except Exception as e:
      summary = 0
  return summary

@register.filter(name='get_device')
def get_device(a, b):
  return [a, b]

