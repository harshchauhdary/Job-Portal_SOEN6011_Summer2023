from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import User
from .forms import UserProfileForm


def login(request):
    from candidate.models import Candidate
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
            else:
                # employer Detail page
                return ""
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
                return render(request, 'users/login.html')
            # save profile data
            u = form.save()
            request.session["user_id"] = u.id
            request.session["is_authenticated"] = True
            if u.role == 'C':
                return HttpResponseRedirect('/candidates/createProfile')
            else:
                # employer Detail page
                return ""
    else:

        form = UserProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'users/register.html', context)
