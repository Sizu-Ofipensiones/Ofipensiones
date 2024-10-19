from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Report

# Detalle de un reporte
class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/report_detail.html'

# Crear un reporte
class ReportCreateView(CreateView):
    template_name = 'reports/report_form.html'
    success_url = reverse_lazy('report_list')
    
    # Defining the fields manually since there's no model
    fields = ['user_id', 'date', 'transactions']

    def form_valid(self, form):
        # You can access the form data like this
        user_id = form.cleaned_data['user_id']
        date = form.cleaned_data['date']
        transactions = form.cleaned_data['transactions']
        
        # Here you could store the data in-memory or pass it to a service, 
        # but since there's no database, no need to save it to a model.
        # For example, print or log the data:
        print(f"Report created with UserID: {user_id}, Date: {date}, Transactions: {transactions}")
        
        # Redirect to the success URL
        return super().form_valid(form)
