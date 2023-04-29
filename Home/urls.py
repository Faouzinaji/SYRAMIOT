from django.urls import path
from . import views
from Home.API import (
    APIDeviceDataCreate, LoginAuthToken, APIDeviceDataUpdate,
    get_dhl_rates_view, get_rates
)


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("date", views.dashboard_date, name="dashboard_date"),
    path("Settings", views.Setting, name="Settings"),
    path("setting_security", views.setting_security, name="setting_security"),
    path("active_devices", views.active_devices, name="active_devices"),
    # devices urls
    path("my_devices", views.my_devices, name="my_devices"),
    path("order_device", views.order_device, name="order_device"),
    path("add_device", views.add_device, name="add_device"),
    path("device_export_csv", views.device_export_csv, name="device_export_csv"),
    path("edit_device/<int:id>", views.edit_device, name="edit_device"),
    path(
        "edit_device_after_activate/<int:id>",
        views.edit_device_after_activate,
        name="edit_device_after_activate",
    ),
    path("delete_device/<int:id>", views.delete_device, name="delete_device"),
    # path('buy_certificate', views.buy_certificate, name='buy_certificate'),
    # path('certificate_payment_success', views.certificate_payment_success,name='certificate_payment_success'),
    # just to add a new device via plain url
    path("api/device/add", views.add_device_api, name="add_device_api"),
    # API for IoT device
    # Login ===================================================================
    path("api/login/", LoginAuthToken.as_view(), name="loginapi"),
    # Create IoT device Data ==================================================
    path(
        "api/device/create/", APIDeviceDataCreate.as_view(),
        name="iot_device_create"
    ),
    # Update IoT device Data ==================================================
    path(
        "api/device/update/<int:pk>/",
        APIDeviceDataUpdate.as_view(),
        name="iot_device_update",
    ),
    # List of IoT Device data =================================================
    path(
        "api/device",
        views.DeviceListCreateViewSet.as_view(),
        name="DeviceListCreateViewSet",
    ),
    # Details of IoT Device data ==============================================
    path(
        "api/device/<int:pk>", views.Device_Details.as_view(),
        name="Device_Details"
    ),
    # API Test ================================================================
    path("api/", get_dhl_rates_view, name="Device_Details"),
    path("api/easy/", get_rates, name="get_rates"),
]
