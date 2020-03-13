from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout as django_logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect, Http404, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import UserLoginForm, SignUpForm, PasswordChangeForm
from django.contrib import messages
# Create your views here.


def login_page(request):
    ''' login view '''

    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    print("accepted details")
    if form.is_valid():
        print('form is valid')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user:
            print('auth is valid')
            login(request, user)
        else:
            print('invalid auth')
            messages.add_message(request,messages.SUCCESS,"Incorrect username or password")
        print('auth')
        if next:
            return redirect(next)
        return redirect('/')
    context = {
        'form': form
    }
    print("home details")
    return render(request,'login.html', context)


@login_required
def logout(request):
    django_logout(request)
    return redirect('/login')


class CreateNewUser(View):
    template = 'create_user.html'
    form_class = SignUpForm
    success_url = reverse_lazy('')

    def get(self, request):
        form = self.form_class(None)
        context = {'form': form,
                   'title': 'CreateNewUser',
                   }
        return render(request, self.template, context)

    def post(self, request ):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('campaign_list')
        else:
            form = SignUpForm()
        return render(request, 'create_user.html', {'form': form})




def alluser(request):
    all_users = get_user_model().objects.all()
    context = {'allusers': all_users}
    return render(request, 'alluser.html', context)


def userdetail(request, name):
    template = 'user-detail.html'
    details = User.objects.get(username=name)
    context = {

        'details': details,
        'title': ' Details',
    }
    return render(request, template, context)




@staff_member_required
def del_user(request, username):
    try:
        u = User.objects.get(username = username)
        u.delete()
        messages.success(request, "The user is deleted")

    except User.DoesNotExist:
        messages.error(request, "User doesn't exist")
        return render(request, 'front.html')

    except Exception as e:
        return render(request, 'front.html',{'err':e.message})

    return render(request, 'front.html')


def changepassword(request):
    if request.method == 'POST':
        # user = User.objects.get(username=user)
        form = PasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })