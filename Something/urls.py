from django.urls import path
from .views import index,custom_logout,Connect,LobbiesView,Join,endrace,activate,activateEmail,garage,carworkshop,Chat,Upgrade,Money_Up_View,Monay_Up_Payment,Drag_Racing,Drag_Racing_Payment

urlpatterns = [
    path('',index.as_view(),name='home'),
    path('garage/',garage.as_view(),name='garage'),
    path('logout/',custom_logout,name='logout'),
    path('activete/',activateEmail,name='act'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('garage/workshop/',carworkshop.as_view(),name='carw'),
    path('garage/workshop/<pk>/upgrade/',Upgrade.as_view(),name='Upg'),
    path('game/money_up/',Money_Up_View.as_view(),name='up'),
    path('game/money_up/<pk>/<token>/<money>/', Monay_Up_Payment.as_view(), name='garage1'),
    path('game/drag_racing/',Drag_Racing.as_view(),name='drag'),
    path('game/drag_racing/<pk>/<token>/<money>/',Drag_Racing_Payment.as_view(),name='drag1'),
    path('game/chat/',Chat.as_view(),name='chat'),
    path("game/lobbis/",LobbiesView.as_view(),name="lobby"),
    path("game/online_1/<room>/",Connect.as_view(),name="room"),
    path("game/online_2/<room>/",Join.as_view(),name="join"),
    path("finish/",endrace,name="end"),
]
