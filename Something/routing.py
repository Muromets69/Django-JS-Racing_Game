from django.urls import path
from .consumers import ChatConsumer,GonkaCons,Con

channels_routing = [
    path('ws/chat/<str:user>/',ChatConsumer.as_asgi()),
    path('ws/gonka/<int:pk>/<str:room>/',GonkaCons.as_asgi()),
    path('ws/gg/',Con.as_asgi()),
]