from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from Comments.models import Comments
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.

model = Comments


class ListComm(ListView):
    queryset = Comments.objects.all()
    template_name = 'Comments/readcomments.html'
    context_object_name = 'Comments' 


class WriteComm(LoginRequiredMixin, CreateView):
    queryset = Comments.objects.all()
    fields = ['comment']
    login_url = 'login'
    template_name = 'Comments/postcom.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(WriteComm, self).form_valid(form)
        

class CommUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    queryset = Comments.objects.all()
    fields = ['comment']
    login_url = 'login'
    template_name = 'Comments/postcom.html'
    success_url = reverse_lazy('list')


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CommUpdate, self).form_valid(form)

    def test_func(self):
        Comments = self.get_object()
        if Comments.user == self.request.user:
            return True
        False


class CommDel(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    queryset = Comments.objects.all()
    fields = ['comment']
    login_url = 'login'
    template_name = 'Comments/deletecom.html'
    success_url = reverse_lazy('home')


    def test_func(self):
        Comments = self.get_object()
        if Comments.user == self.request.user:
            return True

