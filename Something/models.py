from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint

class Enemy(models.Model):
    lvl = models.PositiveSmallIntegerField("LVL")
    car = models.ForeignKey("Car",verbose_name="MYCAR",on_delete=models.SET_NULL,blank=True,default=None,null=True)

    def set_car(self):
        if (self.lvl>20):
            gear=101
            sec=145
            th=200
            fo=270
            fif=300
            six=300+randint(20,40)
        else:
            gear = self.lvl * 15
            sec = gear*1.9
            th = sec*2
            fo = th*1.5
            fif = fo*1.3
            six = fif+25
            turbo = False
        if (self.lvl > 10):
            turbo=True
        car = Car.objects.create(engine=((self.lvl+1)*2),first=gear,second=sec,third=th,fouth=fo,fivth=fif,wheels=2,max_speed=six,turbo=turbo)
        self.car = car

class Car(models.Model):
    name = models.CharField("CAR NAME", max_length=20,default="ZhuGhoul")
    lvl = models.PositiveSmallIntegerField("LVL",default=1)
    engine = models.DecimalField("ENGINE",max_digits=6, decimal_places=2)
    first = models.PositiveIntegerField("GEAR_1")
    second = models.PositiveIntegerField("GEAR_2")
    third = models.PositiveIntegerField("GEAR_3")
    fouth = models.PositiveIntegerField("GEAR_4")
    fivth = models.PositiveIntegerField("GEAR_5")
    max_speed = models.PositiveIntegerField("MAX")
    wheels = models.DecimalField("WHEELS",max_digits=6, decimal_places=2)
    turbo = models.BooleanField("TURBO")

    def upgrade_eng(self):
        return self.engine/5
    
    def sum_eng(self):
        return self.engine+self.upgrade_eng()
    
    def price_gear(self):
        return 1000*self.lvl

    def price_eng(self):
        return 500*self.lvl
    
    def price_wheels(self):
        return 300*self.lvl
    
    def price_turbo(self):
        return 10000*self.lvl//5
    
    def upgrade_gear1(self):
        return self.first//5

    def sum_gear1(self):
        return self.first+self.first//5
    
    def upgrade_gear2(self):
        return self.second//6
    
    def sum_gear2(self):
        return self.second+self.second//6
    
    def upgrade_gear3(self):
        return self.third//8
    
    def sum_gear3(self):
        return self.third+self.third//8
    
    def upgrade_gear4(self):
        return self.fouth//8
    
    def sum_gear4(self):
        return self.fouth+self.fouth//8
    
    def upgrade_gear5(self):
        return self.fivth//8
    
    def sum_gear5(self):
        return self.fivth+self.fivth//8
    
    def upgrade_gear6(self):
        return self.max_speed//10
    
    def sum_gear6(self):
        return self.max_speed+self.max_speed//10
    
    def sum_wheels(self):
        return self.wheels+self.upgrade_wheels()

    def upgrade_wheels(self):
        return self.wheels/5
 

class Newuser(AbstractUser):
    username = models.CharField("username",max_length=50,unique=True,default='NoName')
    ghoul_lvl = models.PositiveIntegerField("POWER",default=1)
    img = models.ImageField("IMG", upload_to='users/',default='users/zxc.jpg')
    balance = models.PositiveIntegerField("BALANCE",default=100)
    active = models.BooleanField("ACTIVE_EMAIL",default=False)
    car = models.ForeignKey("Car",verbose_name="MYCAR",on_delete=models.SET_NULL,blank=True,default=None,null=True)
    enemy = models.ForeignKey("Enemy",verbose_name="ENEMY",on_delete=models.SET_NULL,blank=True,default=None,null=True)

    def set_car(self,start):
        gear = 1 * start
        sec = gear*1.9
        th = sec*1.8
        fo = th*1.3
        fif = fo*1.2
        car = Car.objects.create(engine=2.4,first=gear,second=gear*1.9,third=th,fouth=fo,fivth=fif,wheels=2,max_speed=fif+randint(20,40),turbo=False)
        self.car = car

class Room(models.Model):
    name = models.CharField("ROOM",max_length=50,unique=True)
    player_1 = models.ForeignKey("Newuser",verbose_name="user",on_delete=models.SET_NULL,blank=True,default=None,null=True,related_name='person1')
    player_2 = models.ForeignKey("Newuser",verbose_name="user2",on_delete=models.SET_NULL,blank=True,default=None,null=True,related_name='person2')
    num = models.PositiveSmallIntegerField("Count",default=1)