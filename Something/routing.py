from django.urls import path
from .consumers import ChatConsumer,GonkaCons

channels_routing = [
    path('ws/chat/<str:user>/',ChatConsumer.as_asgi()),
    path('ws/gonka/<int:pk>/<str:room>/',GonkaCons.as_asgi()),
]