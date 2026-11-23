from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Customer, ServicePlan, ServiceOrder


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'phone', 'email', 'national_code', 'company', 'address', 'notes']


class PlanForm(forms.ModelForm):
    class Meta:
        model = ServicePlan
        fields = ['name', 'category', 'duration_months', 'price', 'specs', 'is_active']


class OrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = ['customer', 'plan', 'start_date', 'end_date', 'status', 'account_info', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


@staff_member_required
def customer_list(request):
    q = request.GET.get('q', '').strip()
    customers = Customer.objects.all()
    if q:
        customers = customers.filter(full_name__icontains=q) | customers.filter(phone__icontains=q)
    return render(request, 'services/customers.html', {'customers': customers, 'q': q})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'services/customer_detail.html', {
        'customer': customer,
        'orders': customer.orders.select_related('plan'),
        'invoices': customer.invoices.select_related('plan'),
    })


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully.')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'form.html', {'form': form, 'title': 'New Customer'})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('customer_detail', pk=pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'form.html', {'form': form, 'title': f'Edit: {customer}'})


@login_required
def plan_list(request):
    return render(request, 'services/plans.html', {'plans': ServicePlan.objects.all()})


@login_required
def plan_create(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan created successfully.')
            return redirect('plan_list')
    else:
        form = PlanForm()
    return render(request, 'form.html', {'form': form, 'title': 'New Service Plan'})


@login_required
def order_list(request):
    orders = ServiceOrder.objects.select_related('customer', 'plan')
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    return render(request, 'services/orders.html', {'orders': orders, 'status': status})


@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if not order.end_date:
                order.end_date = order.start_date + timedelta(days=30 * order.plan.duration_months)
            order.save()
            messages.success(request, 'Service created successfully.')
            return redirect('order_list')
    else:
        form = OrderForm(initial={'start_date': timezone.localdate()})
    return render(request, 'form.html', {'form': form, 'title': 'New Service'})


@login_required
def order_renew(request, pk):
    """Renew a service for one more period from the current end date"""
    order = get_object_or_404(ServiceOrder, pk=pk)
    order.end_date = order.end_date + timedelta(days=30 * order.plan.duration_months)
    order.status = 'active'
    order.save()
    messages.success(request, f'Service renewed until {order.end_date}.')
    return redirect('order_list')
