from django.shortcuts import render
from .models import Destination
from .models import Detailed_desc
from .models import pessanger_detail
from .models import Cards
from .models import Transactions 
from .models import NetBanking
from .models import Manager_login
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import *
from django.utils.dateparse import parse_date
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from django import forms
from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.template import Library 
from datetime import datetime
from django.contrib.auth.models import User
import random
 
#  __lte = is eqivelent to lessthan or euivelent
#    table.all().filter().exclude().filer() for two filters and one excluding condition
# Create your views here.

def index(request):
    dests = Destination.objects.all()
    dest1 = []
    j=0
    for i in range(6):
        j=j+2
        temp = Detailed_desc.objects.get(dest_id=j)
        dest1.append(temp)

    return render(request, 'index.html',{'dests': dests, 'dest1' : dest1})

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        #first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, last_name=last_name)
                user.save()
                print('User Created!!!')
                return redirect('login')
        else:
            messages.info(request, 'Password is not matching ')
            return redirect('register')
        return redirect('index')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Sucessfully Logged in')
            email = request.user.email
            print(email)
            content = 'Hello ' + request.user.first_name + ' ' + request.user.last_name + '\n' + 'You are logged in in our site.keep connected and keep travelling.'
            # send_mail('Alert for Login', content
            #           , 'travellotours89@gmail.com', [email], fail_silently=True)
            dests = Destination.objects.all()
            return render(request, 'index.html',{'dests':dests})
        else:
            messages.info(request, 'Invalid credential')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

@login_required(login_url='login')
def destination_list(request,city_name):
    dests = Detailed_desc.objects.all().filter(country=city_name)
    return render(request,'travel_destination.html',{'dests': dests})

@login_required(login_url='login')
def destination_details(request,city_name):
    dest = Detailed_desc.objects.get(dest_name=city_name)
    price = dest.price
    request.session['price'] = price
    request.session['city'] = city_name
    return render(request,'destination_details.html',{'dest':dest})

def search(request):
    try:
        place1 = request.session.get('place')
        print(place1)
        dest = Detailed_desc.objects.get(dest_name=place1)
        print(place1)
        return render(request, 'destination_details.html', {'dest': dest})
    except:
        messages.info(request, 'Place not found')
        return redirect('index')

class KeyValueForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()
    
def pessanger_detail_def(request, city_name):
    KeyValueFormSet = formset_factory(KeyValueForm, extra=1)
    if request.method == 'POST':
        formset = KeyValueFormSet(request.POST)
        if formset.is_valid():
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            date1 = datetime.now().date()
            if temp_date < date1:
                return redirect('index')
            obj = pessanger_detail.objects.get(Trip_id=3)
            pipo_id = obj.Trip_same_id
            #pipo_id =4
            request.session['Trip_same_id'] = pipo_id
            price = request.session['price']
            city = request.session['city']
            print(request.POST['trip_date'])
            #temp_date = parse_date(request.POST['trip_date'])
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            usernameget = request.user.get_username()
            print(temp_date)
            request.session['n']=formset.total_form_count()
            for i in range(0, formset.total_form_count()):
                form = formset.forms[i]

                t = pessanger_detail(Trip_same_id=pipo_id,first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                                     age=form.cleaned_data['age'],
                                     Trip_date=temp_date,payment=price,username=usernameget,city=city)
                t.save()
                # print (formset.forms[i].form-[i]-value)

            obj.Trip_same_id = (pipo_id + 1)
            obj.save()
            no_of_person = formset.total_form_count()
            price1 = no_of_person * price
            GST = price1 * 0.18
            GST = float("{:.2f}".format(GST))
            final_total = GST + price1
            request.session['pay_amount'] = final_total
            return render(request,'payment.html', {'no_of_person': no_of_person,
                                                   'price1': price1, 'GST': GST, 'final_total': final_total,'city': city })
    else:
        formset = KeyValueFormSet()

        return render(request, 'sample.html', {'formset': formset, 'city_name': city_name, })

 
def upcoming_trips(request):
    username = request.user.get_username()
    date1=datetime.now().date()
    person = pessanger_detail.objects.all().filter(username=username)
    person = person.filter(Trip_date__gte=date1)
    print(date1)
    return render(request,'upcoming trip1.html',{'person':person})

def delete_uptrip(request,first_name):
    person = pessanger_detail.objects.get(first_name=first_name)
    person.delete()
    #messages.success(request,"Trip Deleted Successfuly")
    return redirect('index')

@login_required(login_url='login')
def card_payment(request):
    card_no = request.POST.get('card_number')
    pay_method = 'Debit card'
    MM = request.POST['MM']
    YY = request.POST['YY']
    CVV = request.POST['cvv']

    request.session['dcard'] = card_no
    try:
        balance = Cards.objects.get(Card_number=card_no, Ex_month=MM, Ex_Year=YY, CVV=CVV).Balance
        request.session['total_balance'] = balance
        mail1 = Cards.objects.get(Card_number=card_no, Ex_month=MM, Ex_Year=YY, CVV=CVV).email
        return render(request, 'confirmetion_page.html')   

    except:
        return render(request, 'confirmetion_page.html')

@login_required(login_url='login')
def data_fetch(request):
    username = request.user.get_username()
    person = pessanger_detail.objects.all().filter(username=username)

def manager(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if Manager_login.objects.filter(password = password):
            if Manager_login.objects.filter(username = username):
                messages.info(request, 'valid credential')
                return redirect('manager_home')
            else:
                messages.info(request, 'Invalid username')
                return redirect('manager')
        else:
            messages.info(request, 'Invalid password')
            return redirect('manager')
    else:                
     return render(request,'manager.html')

def manager_home(request):
    dests = Destination.objects.all()
    return render(request,'manager_home.html',{'dests': dests})

def add_destination(request):
    if request.method == 'POST':
        m = Destination()
        m.id = request.POST.get('id')
        m.country = request.POST.get('country')
        if len(request.FILES) != 0:
            m.img1 = request.FILES['img1']
            m.img2 = request.FILES['img2']
        m.save()
        messages.info(request, 'Successfully added!!!')
    return render(request,'add_destination.html')

def add_package(request):
    if request.method == 'POST':
        m = Detailed_desc()
        m.country = request.POST.get('country')
        m.days = request.POST.get('days')
        m.price = request.POST.get('price')
        m.rating = request.POST.get('rating')
        m.dest_name = request.POST.get('dest_name')
        m.desc = request.POST.get('desc')
        m.day1 = request.POST.get('day1')
        m.day2 = request.POST.get('day2')
        m.day3 = request.POST.get('day3')
        m.day4 = request.POST.get('day4')
        m.day5 = request.POST.get('day5')
        m.day6 = request.POST.get('day6')
        if len(request.FILES) != 0:
            m.img1 = request.FILES['img1']
            m.img2 = request.FILES['img2']
        m.save()
        messages.info(request, 'Successfully Added!!!')
    return render(request,'add_package.html')

def manager_pack(request):
    pack = Detailed_desc.objects.all()
    return render(request,'manager_pack.html',{'pack': pack})

def edit_desti(request,pk):
    d = Destination.objects.get(id=pk)

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(d.image) > 0:
                os.remove(d.image.path)
            d.img1 = request.POST.get('img1')
            d.img2 = request.POST.get('img2')
        
        d.country = request.POST.get('country')
        d.number = request.POST.get('number')
        d.save()
        messages.info(request, "Product Updated Successfully")
        return redirect('manager_home')
    return render(request, 'edit_desti.html',{'d':d})

def edit_pacakage(request,dest_name):
    p = Detailed_desc.objects.get(dest_name=dest_name)

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(p.image) > 0:
                os.remove(p.image.path)
            p.img1 = request.POST.get('img1')
            p.img2 = request.POST.get('img2')
        
        p.country = request.POST.get('country')
        p.days = request.POST.get('days')
        p.price = request.POST.get('price')
        p.rating = request.POST.get('rating')
        p.dest_name = request.POST.get('dest_name')
        p.desc = request.POST.get('desc')
        p.day1 = request.POST.get('day1')
        p.day2 = request.POST.get('day2')
        p.day3 = request.POST.get('day3')
        p.day4 = request.POST.get('day4')
        p.day5 = request.POST.get('day5')
        p.day6 = request.POST.get('day6')
        p.save()
        messages.info(request, "Product Updated Successfully")
        return render(request,'edit_pacakages.html')

    return render(request, 'edit_pacakages.html',{'p':p})

#DELETE DESTINATION
def deleteProduct(request, pk):
    d = Destination.objects.get(id=pk)
    d.delete()
    messages.success(request,"Product Deleted Successfuly")
    return redirect('manager_home')

#DELETE PACKAGE
def deleteProduct1(request, dest_name):
    p = Detailed_desc.objects.get(dest_name=dest_name)
    p.delete()
    messages.success(request,"Product Deleted Successfuly")
    return redirect('manager_pack')