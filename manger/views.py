import json

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from learn import load_trained_file, prediction_result
from manger.models import Resume

from manger.forms import ResumeCreateForm


def index(request):
    return render(request, 'manger/index.html')


@login_required
def dashboard(request):
    return render(request, 'manger/dashboard.html')


def signout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import render, redirect


User = get_user_model()


def signup(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password1 = request.POST['password1'].strip()
        password2 = request.POST['password2'].strip()
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        email = request.POST['email'].strip()

        if not username:
            errors['username'] = "Username Field is Required!"
        elif len(username) <= 7:
            errors['username'] = "Username must have a length of at least 8 characters!"
        else:
            is_used = User.objects.filter(username=username).exists()
            if is_used:
                errors['username'] = "This Username is already taken!"

        if not password1:
            errors['password1'] = "Password1 is Required!"
        elif len(password1) <= 7:
            errors['password1'] = "Password must have a length of at least 8 characters!"
        if not password2:
            errors['password2'] = "Password2 is Required!"
        if password1 and password2 and password1 != password2:
            errors['password1'] = "Passwords Do not Match!!!"

        if not email:
            errors['email'] = "Email Field is Required!"
        else:
            is_used = User.objects.filter(email=email).exists()
            if is_used:
                errors['email'] = "This Email is already taken!"

        if not first_name:
            errors['first_name'] = "First Name Field is Required!"
        is_valid = len(errors.keys()) == 0
        if is_valid:
            # create user!
            user = User.objects.create_user(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password1
            )
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            return redirect('/?signup=successful')
    context = {
        'errors': errors
    }
    return render(request, 'signup.html', context)


@method_decorator(login_required, "dispatch")
class CreateResume(UpdateView):
    model = Resume
    form_class = ResumeCreateForm

    def get_object(self, queryset=None):
        return Resume.objects.filter(user=self.request.user).first()

    def get_success_url(self):
        return "/?s=1"

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, "dispatch")
class ListResume(ListView):
    model = Resume
    context_object_name = 'objects_list'

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


@method_decorator(login_required, "dispatch")
class DetailResume(DetailView):
    model = Resume
    template_name = 'manger/resume_list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        qs = Resume.objects.all()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = self.get_queryset()
        return super().get_context_data(**kwargs)


@method_decorator(login_required, "dispatch")
@method_decorator(user_passes_test(lambda user: user.is_superuser), "dispatch")
class ListAllResume(ListView):
    model = Resume
    template_name = 'manger/resume_list.html'
    context_object_name = 'objects_list'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = self.get_queryset()
        return super().get_context_data(**kwargs)


def predict(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    extracted_traits = resume.get_personality_values()
    model = load_trained_file()
    # 'Female' = 0;  'Male' = 1
    results = prediction_result(model, resume.fullname, resume.resume.path, personality_values=(
        # openness,neuroticism,conscientiousness,agreeableness,extraversion
        # 0, 22, 7, 4, 7, 3, 2
        resume.gender,
        resume.age,
        extracted_traits['Openness'] * 10,
        extracted_traits['Neuroticism'] * 10,
        extracted_traits['Conscientiousness'] * 10,
        extracted_traits['Agreeableness'] * 10,
        extracted_traits['Extroversion'] * 10,
        # 0, 18, 6, 6, 5, 4, 4
    ))
    if 'CV Location' in results:
        results['CV Location'] = resume.resume.name
    results['extracted_traits'] = extracted_traits

    results = json.dumps(results, indent=4)
    resume.response = results
    resume.save()
    return redirect(reverse('DetailResume', kwargs={'pk': pk}))


