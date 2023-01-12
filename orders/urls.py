from django.urls import path

from orders.views import (CancelledView, OrderCreateView, OrderDetailView,
                          OrderListView, SuccessView)

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order'),
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccessView.as_view(), name='order_success'),
    path('order-cancelled/', CancelledView.as_view(), name='order_cancelled'),

]
