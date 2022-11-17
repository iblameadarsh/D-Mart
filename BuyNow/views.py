from django.views.generic import ListView, DetailView
from .models import Product
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

model = Product


class Read(ListView):
    queryset = Product.objects.all()
    template_name = 'BuyNow/BuyNow.html'
    context_object_name = 'Product'


class ProDetail(DetailView):
    queryset = Product.objects.all()
    template_name = 'BuyNow/detail.html'
    context_object_name = 'Product'


class Write(LoginRequiredMixin, CreateView):
    queryset = Product.objects.all()
    template_name = 'BuyNow/Listing.html'
    fields = ['name', 'description', 'price', 'image', 'category']
    success_url = reverse_lazy('home')
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Write, self).form_valid(form)


class ProUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    queryset = Product.objects.all()
    fields = ['name', 'description', 'price', 'image', 'category']
    template_name = 'BuyNow/Listing.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProUpdate, self).form_valid(form)

    def test_func(self):
        Product = self.get_object()
        if self.request.user == Product.user:
            return True
        False


class DeletePro(LoginRequiredMixin, DeleteView):
    queryset = Product.objects.all()
    template_name = 'BuyNow/Product_confirm_delete.html'
    fields = ['name', 'description', 'price', 'image', 'category']
    success_url = reverse_lazy('home')
    login_url = 'login'

    def test_func(self):
        Product = self.get_object()
        if self.request.user == Product.user:
            return True
        False

# def home(request):
#     title = 'Home'
#     context= {
#         'ListProduct': Product.objects.all()
#     }   
#     return render(request, 'BuyNow/home.html',context)