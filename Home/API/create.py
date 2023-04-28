from rest_framework.permissions import (IsAuthenticated)
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from django.utils.translation import gettext_lazy as _
from Home.serializers import DeviceSerializer, AuthCustomTokenSerializer
from Home.models import API_Device_data


class LoginAuthToken(ObtainAuthToken):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def post(self, request, *args, **kwargs):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'message': "You are successfully logged in",
            'status': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


class APIDeviceDataCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = DeviceSerializer
    queryset = API_Device_data.objects.all()

    def post(self, request, *args, **kwargs):
        """
        This method is used to create the laboratory test results.
        """
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED,
                headers=headers
            )
        except Exception as e:
            print(e)
            return Response(
                {'error': _('Something went wrong')},
                status=status.HTTP_400_BAD_REQUEST
            )


class APIDeviceDataUpdate(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = DeviceSerializer
    queryset = API_Device_data.objects.all()

    def put(self, request, *args, **kwargs):
        """
        This method is used to update the IoT device Data.
        """
        serial_no = request.data.get('serial_no')
        device_password = request.data.get('device_password')
        date = request.data.get('date')
        time = request.data.get('time')
        hours = request.data.get('hours')
        count_input = request.data.get('count_input')
        count_output = request.data.get('count_output')
        state = request.data.get('state')
        cadence = request.data.get('cadence')
        stop = request.data.get('stop')
        mtbf = request.data.get('mtbf')
        mttr = request.data.get('mttr')
        try:
            instance = self.get_object()
            api_device = API_Device_data.objects.get(pk=instance.pk)
            if serial_no:
                api_device.serial_no = serial_no
            if device_password:
                api_device.device_password = device_password
            if date:
                api_device.date = date
            if time:
                api_device.time = time
            if hours:
                api_device.hours = hours
            if count_input:
                api_device.count_input = count_input
            if count_output:
                api_device.count_output = count_output
            if state:
                api_device.state = state
            if cadence:
                api_device.cadence = cadence
            if stop:
                api_device.stop = stop
            if mtbf:
                api_device.mtbf = mtbf
            if mttr:
                api_device.mttr = mttr
            api_device.save()
            return Response(
                {
                    'Data': {
                        'api_device': api_device.serial_no,
                        'device_password': api_device.device_password,
                        'date': api_device.date,
                        'time': api_device.time,
                        'hours': api_device.hours,
                        'count_input': api_device.count_input,
                        'count_output': api_device.count_output,
                        'state': api_device.state,
                        'cadence': api_device.cadence,
                        'stop': api_device.stop,
                        'mtbf': api_device.mtbf,
                        'mttr': api_device.mttr
                    },
                    'success': _('Community Based Water Supply Updated.'),
                    'status': status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                {'error': _('Something went wrong')},
                status=status.HTTP_400_BAD_REQUEST
            )
