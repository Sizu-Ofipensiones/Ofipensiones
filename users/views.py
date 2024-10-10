from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import User

# Lista de usuarios
class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

# Detalle de un usuario
class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'

# Crear un usuario
class UserCreateView(CreateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['name', 'email', 'password', 'position']
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = form.cleaned_data['password']  # Si deseas, puedes encriptar la contraseña
        user.save()
        return super().form_valid(form)

# Actualizar un usuario
class UserUpdateView(UpdateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['name', 'email', 'position']
    success_url = reverse_lazy('user_list')

# Eliminar un usuario
class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
