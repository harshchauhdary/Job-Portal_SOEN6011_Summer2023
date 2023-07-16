from django.shortcuts import render
from .models import Candidate


def login(request):

    if request.method == 'POST':

        login_data = request.POST.dict()
        username = login_data.get("username")
        password = login_data.get("password")
        user_type = login_data.get("user_type")

        c = Candidate.objects.get(username=username)
        if c.password == password:
            request.session["user_id"] = c.id
            request.session["is_authenticated"] = True
            return render(request, 'candidates/candidateDetailTemplate.html', context={'candidate': c})
        else:
            return render(request, 'authentication/login.html')

    else:

        return render(request, 'authentication/login.html')
