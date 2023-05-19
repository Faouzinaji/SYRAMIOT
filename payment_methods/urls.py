from django.urls import path
from . import views


urlpatterns = [
    path('payment_success', views.stripe_payment_success,name='thanks_page'),
    path('history/', views.PaymentHistory.as_view(),name='payment_history'),
    path(
        'order_payment_success', views.stripe_buy_devices_payment_success,
        name='buy_devices_thanks_page'
    ),
    path('payment_cancel', views.payment_cancel,name='sorry_page'),
    path('checkout',views.checkout,name='checkout'),
    path('checkout_page',views.checkout_page,name='checkout_page'),
    path('checkout_session/<int:billing_id>',views.checkout_session,name='checkout_session'),
    path('buy_devices',views.checkout_session_for_buy_devices,name='buy_devices'),
]