from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import User
from .forms import UserProfileForm


def login(request):
    from candidate.models import Candidate
    from employer.models import Employer
    if request.method == 'POST':

        login_data = request.POST.dict()
        email = login_data.get("email")
        password = login_data.get("password")
        try:
            u = User.objects.get(email=email)
        except Exception:
            return render(request, 'users/login.html')

        if u.password == password:
            request.session["user_id"] = u.id
            request.session["is_authenticated"] = True
            request.session["email"] = u.email
            if u.role == 'C':
                try:
                    c = Candidate.objects.filter(user=u.id)[0]
                    request.session["c_id"] = c.id
                    del request.session["user_id"]
                    return HttpResponseRedirect('/candidates/profile')
                except Exception:
                    return HttpResponseRedirect('/candidates/createProfile')
                
            elif u.role == 'A':
                request.session["a_id"] = request.session["user_id"]
                del request.session["user_id"]
                return HttpResponseRedirect('/csaadmin/home')
                
            else:
                try:
                    # employer Detail page
                    e = Employer.objects.filter(userID=u.id)[0]
                    request.session["e_id"] = e.id
                    del request.session["user_id"]
                    return HttpResponseRedirect("/employer/profile/")
                except Exception:
                    return HttpResponseRedirect('/employer/profile/create')
        else:
            return render(request, 'users/login.html')

    else:

        return render(request, 'users/login.html')


# register
def registration(request):

    if request.method == 'POST':

        form = UserProfileForm(request.POST)

        if form.is_valid():

            if User.objects.filter(email=form.cleaned_data["email"]).count() != 0:
                return render(request, '/')
            if form.cleaned_data["role"] == 'A':
                return render(request, '/register.html')
            # save profile data
            u = form.save()
            request.session["user_id"] = u.id
            request.session["is_authenticated"] = True
            if u.role == 'C':
                return HttpResponseRedirect('/candidates/createProfile')
            else:
                # employer Detail page
                # request.session["e_id"] = u.id
                return HttpResponseRedirect('/employer/profile/create/')
    else:

        form = UserProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'users/register.html', context)

# logout


def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    if "e_id" in request.session:
        del request.session["e_id"]
    if "c_id" in request.session:
        del request.session["c_id"]
    if "a_id" in request.session:
        del request.session["a_id"]
    del request.session["is_authenticated"]

    return HttpResponseRedirect('/')
