# from operator import is_not
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm


# from django.contrib.auth import login
# from django.contrib import messages


class WeLogin(LoginView):
    template_name = 'Users/Login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    # messages.success(request, "Welcome to the Django-Mart!")

    def get_success_url(self):
        return reverse_lazy('home')


class Signup(FormView):
    template_name = 'Users/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        # if user  is not None:
        #     login(self.request,user)
        return super(Signup, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('login')
