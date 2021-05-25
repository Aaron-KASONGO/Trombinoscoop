from django.shortcuts import render, redirect
from .forms import LoginForm, StudentProfileForm, EmployeeProfileForm
from .models import Person, Student, Employee


def welcome(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        return render(request, 'welcome.html', {'logged_user': logged_user})
    else:
        return redirect('/login')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            logged_user = Person.objects.get(email=user_email)
            request.session['logged_user_id'] = logged_user.id
            return redirect('/welcome')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST' and 'profileType' in request.POST:
        studentForm = StudentProfileForm(prefix="st")
        employeeForm = EmployeeProfileForm(prefix="em")
        if request.POST['profileType'] == 'student':
            studentForm = StudentProfileForm(request.POST, prefix="st")
            if studentForm.is_valid():
                studentForm.save()
                return redirect('/login')
        elif request.POST['profileType'] == 'employee':
            employeeForm = EmployeeProfileForm(request.POST, prefix="em")
            if employeeForm.is_valid():
                employeeForm.save()
                return redirect('/login')
        # Le formulaire envoyé n'est pas valide
        return render(request, 'user_profile.html', {'studentForm': studentForm, 'employeeForm': employeeForm})
    else:
        studentForm = StudentProfileForm(prefix="st")
        employeeForm = EmployeeProfileForm(prefix="em")
        return render(request, 'user_profile.html', {'studentForm': studentForm, 'employeeForm': employeeForm})


def get_logged_user_from_request(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']

        if len(Student.objects.filter(id=logged_user_id)) == 1:
            return Student.objects.get(id=logged_user_id)
        elif len(Employee.objects.filter(id=logged_user_id)) == 1:
            return Employee.objects.get(id=logged_user_id)
        else:
            return None
    else:
        return None
