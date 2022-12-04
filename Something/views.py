from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import View,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from .tokens import account_activation_token,moneytoken
from .models import Enemy,Room
from .forms import Form_Dist,CreateRoom


class index(View):
    def get(self,request):
        return render(request=request,template_name='home.html',context={"text":'Home'})

class carworkshop(View,LoginRequiredMixin):
    def get(self,request):
        if self.request.user.is_authenticated==False:
            return redirect('account_login')
        return render(request=request,template_name='carw.html')
           
class garage(View,LoginRequiredMixin):
    def get(self,request):
        if self.request.user.is_authenticated==False:
            return redirect('account_login')
        if request.user.car==None:
            request.user.set_car(20)
            request.user.save()
        return render(request=request,template_name='garage.html',context={'form':Form_Dist()})

class Upgrade(View,LoginRequiredMixin):
    def post(self,request,pk):
        pk = int(pk)
        if self.request.user.is_authenticated==False:
            return redirect('account_login')
        if pk == 1:    
            if self.request.user.balance>=self.request.user.car.price_eng():
                self.request.user.car.engine=self.request.user.car.sum_eng()
                self.request.user.balance-=self.request.user.car.price_eng()
                self.request.user.car.lvl+=1
                self.request.user.car.save()
                self.request.user.save()
                return redirect('carw')
            else:
                return render(request=request,template_name='error.html',context={"mess":"Not enough money!"})
        elif pk == 2:
            if self.request.user.balance>=self.request.user.car.price_gear():
                self.request.user.balance-=self.request.user.car.price_gear()
                self.request.user.car.first=self.request.user.car.sum_gear1()
                self.request.user.car.second=self.request.user.car.sum_gear2()
                self.request.user.car.third=self.request.user.car.sum_gear3()
                self.request.user.car.fouth=self.request.user.car.sum_gear4()
                self.request.user.car.fivth=self.request.user.car.sum_gear5()
                self.request.user.car.max_speed=self.request.user.car.sum_gear6()
                self.request.user.car.lvl+=1
                self.request.user.car.save()
                self.request.user.save()
                return redirect('carw')
            else:
                return render(request=request,template_name='error.html',context={"mess":"Not enough money!"})
        elif pk == 3:
            if self.request.user.balance>=self.request.user.car.price_wheels():
                self.request.user.balance-=self.request.user.car.price_wheels()
                self.request.user.car.wheels = self.request.user.car.sum_wheels()
                self.request.user.car.lvl+=1
                self.request.user.car.save()
                self.request.user.save()
                return redirect('carw')
            else:
                return render(request=request,template_name='error.html',context={"mess":"Not enough money!"})
        elif pk == 4:
            if self.request.user.balance>=self.request.user.car.price_turbo():
                self.request.user.balance-=self.request.user.car.price_turbo()
                self.request.user.car.lvl+=1
                self.request.user.car.turbo = True
                self.request.user.car.save()
                self.request.user.save()
                return redirect('carw')
            else:
                return render(request=request,template_name='error.html',context={"mess":"Not enough money!"})
        else:
            return render(request=request,template_name='error.html',context={"mess":"Don`t have this upgrade"})

class Money_Up_View(View,LoginRequiredMixin):
    def get(self,request):
        token = moneytoken.make_token(request.user)
        return render(request=request,template_name='money_up.html',context={"token":token})   

class Monay_Up_Payment(View,LoginRequiredMixin,UserPassesTestMixin):
    def get(self,request,*args,**kwargs):
        user = get_user_model().objects.get(pk=kwargs['pk'])
        user.balance += int(kwargs['money'])
        user.save()
        return redirect(reverse_lazy('garage'))

    def test_func(self):
        own = get_user_model().objects.get(pk=self.kwargs['pk'])
        return moneytoken.check_token(self.request.user,self.kwargs['token']) and self.request.user == own

class Drag_Racing(View,LoginRequiredMixin):
    def get(self,request):
        token = moneytoken.make_token(request.user)
        enemy = Enemy.objects.create(lvl = request.user.ghoul_lvl)
        enemy.set_car()
        size = request.GET['select']
        print(size)
        print(type(size))
        return render(request=request, template_name="gonka_b.html",context={"token":token,"enemy":enemy,'size':size,'token':token})

class Drag_Racing_Payment(View,LoginRequiredMixin,UserPassesTestMixin):
    def get(self,request,*args,**kwargs):
        user = get_user_model().objects.get(pk=kwargs['pk'])
        user.balance += int(kwargs['money'])
        if int(kwargs['money'])>0:
            user.ghoul_lvl += 1
        user.save()
        return redirect(reverse_lazy('garage'))

    def test_func(self):
        own = get_user_model().objects.get(pk=self.kwargs['pk'])
        return moneytoken.check_token(self.request.user,self.kwargs['token']) and self.request.user == own

class Chat(View):
    def get(self,req):
        if self.request.user.is_authenticated==False:
            return redirect('account_login')
        return render(request=req, template_name="chat.html")
    
class LobbiesView(View):
    def get(self,req):
        if self.request.user.is_authenticated==False:
            return redirect('account_login')
        try:
            room = Room.objects.get(player_1=req.user)
            room.delete()
        except Room.DoesNotExist:
            pass
        rooms = Room.objects.all().filter(num=1)
        if len(rooms)>0:
            rm = True
        else:
            rm = False
        return render(request=req, template_name='lobbys.html', context={'rooms':rooms,"form":CreateRoom(),'rooms_len':rm})
    
    def post(self,req):
        room_name = req.POST['name']
        Room.objects.create(name=room_name,player_1=req.user)
        return redirect(reverse_lazy("room",kwargs={"room":room_name}))
    
class Connect(View):
    def get(self,req,*args, **kwargs):
        try:
            Room.objects.get(name=kwargs['room'])
        except Room.DoesNotExist:
            return redirect("lobby")
        return render(request=req, template_name="online.html", context={"room":kwargs['room']})
    
class Join(View):
    def get(self,req,*args, **kwargs):
        try:
            room = Room.objects.get(name=kwargs['room'])
        except Room.DoesNotExist:
            return redirect("lobby")
        user = room.player_1
        room.player_2 = self.request.user
        room.num += 1
        room.save()
        return render(request=req, template_name="join.html", context={"room":kwargs['room'],'enemy':user})
    
def endrace(request):
    try:
        room = Room.objects.get(player_1=request.user)
        room.delete()
        return redirect("garage")
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(player_2=request.user)
            room.player_2 = None
            room.num -= 1
            room.save()
        except Room.DoesNotExist:
            pass
        return redirect("garage")

class DetailUserView(DetailView):
    template_name = "detail.html"
    model = get_user_model()
    context_object_name = "useri"

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")

def activateEmail(request):
    if request.user.active:
        return render(request=request,template_name='home.html',context={"text":"Error with sending message!"})
    else:
        token = account_activation_token.make_token(request.user)
        uid64 = force_str(urlsafe_base64_encode(force_bytes(request.user.pk)))
        url = '127.0.0.1:8000' + reverse_lazy('activate',kwargs={'uidb64':uid64,'token':token})

        send_mail('Активация email',
        f"Здравствуйте <b>{request.user.username}</b>! Для активации акаунта перейдите по ссылке: {url}",
        "pososi@gmail.com", [request.user.email,],
        fail_silently=False    
        )
        return render(request=request,template_name='error.html',context={"mess":"Check your mail"})

        

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('home')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect("home")