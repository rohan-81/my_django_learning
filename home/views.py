from django.shortcuts import render,redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
# Learning Git

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass')
        try:
            uname=User.objects.filter(email=email).first().username
        
        except Exception as e:
            return render(request, 'regestration/log-in.html', {'error': 'No such Email Id registered!!'})

        user = authenticate(request,username=uname,password=password)
        print("email :",email,"\nuser :",user)

        if user is not None:
            request.session['user_id'] = user.id
            request.session['email'] = user.email
            request.session['is_logged_in'] = True
            login(request, user)  
            return redirect('home')
        else:
            return render(request, 'regestration/log-in.html', {
                'error': 'Invalid Password or email !!'
            })

    return render(request, 'regestration/log-in.html')

def signup_page(request):
    if request.method=="POST":
        username=request.POST.get('uname')
        email=request.POST.get('email')
        phone=request.POST.get('number')
        dob=request.POST.get('dob')
        password1=request.POST.get('pass1')
        password2=request.POST.get('pass2')
        gen=request.POST.get('gen')
        address=request.POST.get('address')

        thisyear=datetime.now().strftime("%Y")
        print(thisyear)
        age=int(thisyear)-int(dob[:4])


        if username:
            if User.objects.filter(username=username).exists():
                return render(request, 'regestration/sign-up.html', {'error':'Username already exists'})
            else:
                if password1!=password2:
                    return render(request, 'regestration/sign-up.html', {'error':'Passwords not matched! '})
                else:
                    if len(password1)<8:
                        return render(request, 'regestration/sign-up.html', {'error':'Password must be of 8 characters!'})
                    else:
                        if not email:
                            return render(request, 'regestration/sign-up.html', {'error':'Email is required!'})
                        else:
                            if User.objects.filter(email=email).exists():
                                return render(request, 'regestration/sign-up.html', {'error':'Email already registered!'})
                            else:
                                if age>16:
                                    new_user=User.objects.create_user(username=username,email=email,password=password1)
                                    UserProfile.objects.create(user=new_user,email=email,number=phone,dob=dob,age=age,gender=gen,address=address)
                                    return redirect('login')
                                else:
                                    return render(request, 'regestration/sign-up.html', {'error':'Age should be above 16!'})
    return render(request, 'regestration/sign-up.html')

def logout_page(request):
    request.session.flush()
    return redirect('login')



@login_required(login_url='login')
def home_page(request):
    print(f"user : {request.user}\nIs_staff : {request.user.is_staff}")
    print(request.user.get_username())
    
    
    if request.method == 'POST':
        title_from_form = request.POST.get('task_title')
        if title_from_form:
            Task.objects.create(user=request.user, title=title_from_form)
            return redirect('home')

    all_tasks = Task.objects.filter(user=request.user).order_by("-id")
    context = {'tasks': all_tasks}

    return render(request, 'dashboard/index.html', context)



@login_required(login_url='login')
def profile_page(request):
    total_tasks = Task.objects.filter(user=request.user).count()

    profile=UserProfile.objects.get(user=request.user)
    thisyear=datetime.now().strftime("%Y")


    print(thisyear)
    age=int(thisyear)-int(profile.dob.year)
    print(int(profile.dob.year))
    profile.age=age
    profile.save()


    context = {
        'total_tasks': total_tasks
    }
    return render(request, 'Profile/profile.html', context)



@login_required(login_url='login')
def update_profile(request):
    user = request.user
    profile=UserProfile.objects.get(user=user)

    if request.method == 'POST':
        new_username = request.POST.get('username').strip()
        new_email = request.POST.get('email').strip()
        new_number = request.POST.get('number')
        new_address = request.POST.get('address')
        
        # Check if username is taken by another user
        if User.objects.filter(username=new_username).exclude(id=user.id).exists():
            error = "This username is already taken."
        elif not new_username:
            error = "Username cannot be empty."
        else:
            if new_number:
                new_number = int(new_number)
                profile.number = new_number
            else:
                new_number = profile.number

            user.username = new_username
            user.email = new_email
            profile.email=new_email
            profile.address = new_address
            user.save()
            profile.save()
            return redirect('profile')

    return render(request, 'Profile/update_profile.html')


@login_required(login_url='login')
def delete_task(request,task_id):
    if request.method=='POST':
        user = request.user
        task=get_object_or_404(Task, id=task_id, user=user)
        task.delete()
        task.save()
        return redirect('home')

login_required(login_url='login')
def setting_page(request):
    error=None
    user=User.objects.get(username=request.user.username)
    if request.method == 'POST':
        old_password = request.POST.get('pass')
        new_password = request.POST.get('pass1')
        confirm_password = request.POST.get('pass2')
        print(user.check_password(old_password))
        
        if user.check_password(old_password):
            if new_password==confirm_password:
                if len(new_password)>=8:
                    user.set_password(new_password)
                    user.save()
                    request.session.flush()
                    return redirect('logout')
                else:
                    error="Password must be 8 character long!"
            else:
                error="New and confirm password not matched!"
        else:
            error="Old password is incorrect!"
        
    return render(request, 'dashboard/setting.html',{'error':error})