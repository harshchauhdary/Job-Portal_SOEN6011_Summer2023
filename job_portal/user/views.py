from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import User
from .forms import UserProfileForm


def login(request):

    if request.method == 'POST':

        login_data = request.POST.dict()
        username = login_data.get("username")
        password = login_data.get("password")
        user_type = login_data.get("user_type")

        c = User.objects.get(username=username)
        if c.password == password:
            request.session["user_id"] = c.id
            request.session["is_authenticated"] = True
            return render(request, 'candidates/candidateDetailTemplate.html', context={'candidate': c})
        else:
            return render(request, 'users/login.html')

    else:

        return render(request, 'users/login.html')


# View and Save profile data
def create_Profile(request):

    if request.method == 'POST':

        form = UserProfileForm(request.POST)

        if form.is_valid():
            # save profile data
            form.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/users/profile')

    else:

        form = UserProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'users/profileFormTemplate.html', context)


# Update profile
def update_profile(request):
    # get candidate id from session
    if 'user_id' in request.session:
        cpk = request.session['user_id']
    else:
        return render(request, 'users/login.html')

    user = get_object_or_404(User, pk=cpk)

    if request.method == 'POST':

        form = UserProfileForm(request.POST)

        if form.is_valid():
            # save profile data
            user.firstname = form.cleaned_data['firstname']
            user.lastname = form.cleaned_data['lastname']
            user.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/users/profile/')

    else:

        form = UserProfileForm(
            initial={'firstname': user.firstname, 'lastname': user.lastname})

    context = {
        'form': form,
        'user': user,

    }

    return render(request, 'users/updateProfileTemplate.html', context)


# view profile
def view_Profile(request):
    # get user id from session
    if 'user_id' in request.session:
        cpk = request.session['user_id']
    else:
        return render(request, 'users/login.html')
    user = get_object_or_404(User, pk=cpk)
    return render(request, 'users/userDetailTemplate.html', context={'user': user})
