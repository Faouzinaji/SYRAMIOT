from Home.models import API_Device_data


def delete_data():
    API_Device_data.objects.all().delete()

# delete_data()
