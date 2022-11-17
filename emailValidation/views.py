# from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import EmailValidations
from django.urls import reverse_lazy
from emailValidation.tasks import run_export
# from emailValidation.supplier_email_verify import EmailProcess

# Create your views here.

model = EmailValidations


class FormHandler(LoginRequiredMixin, CreateView):
    model = EmailValidations
    queryset = EmailValidations.objects.all()
    fields = [
        'taskName',
        'rcpt_email',
        'input_file'
    ]
    template_name = 'emailValidation/emailValidForm.html'
    context_object_name = EmailValidations
    success_url = reverse_lazy('home')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(FormHandler, self).form_valid(form)


class ViewForm(DetailView):
    template_name = 'emailValidation/fromView.html'
    queryset = EmailValidations.objects.all()
    context_object_name = 'EmailValidations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['EmailValidations'] = context['EmailValidations'].filter(user=self.request.user)
        return context

    def expo_file(self, request):
        data = self.request.data
        run_export.delay()
        pass
