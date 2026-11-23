from django import forms
from accounts.permissions import role_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Invoice, Payment
from services.models import ServiceOrder


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'plan', 'amount', 'discount', 'due_date', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'min': '0'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'method', 'reference']


@role_required('finance', 'admin')
def invoice_list(request):
    invoices = Invoice.objects.select_related('customer', 'plan')
    status = request.GET.get('status')
    if status:
        invoices = invoices.filter(status=status)
    return render(request, 'invoices/list.html', {'invoices': invoices, 'status': status})


@role_required('finance', 'admin')
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice.objects.select_related('customer', 'plan'), pk=pk)
    paid = sum(p.amount for p in invoice.payments.all())
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=Payment(invoice=invoice, recorded_by=request.user))
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.recorded_by = request.user
            payment.save()
            messages.success(request, 'Payment recorded.')
            return redirect('invoice_detail', pk=pk)
    else:
        form = PaymentForm(instance=Payment(invoice=invoice), initial={'amount': max(invoice.total - paid, 0)})
    return render(request, 'invoices/detail.html', {
        'invoice': invoice, 'paid': paid, 'remaining': invoice.total - paid,
        'payments': invoice.payments.all(), 'form': form,
    })


@role_required('finance', 'admin')
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            if not invoice.due_date:
                invoice.due_date = timezone.localdate() + timedelta(days=7)
            invoice.save()
            messages.success(request, f'Invoice {invoice.invoice_number} issued.')
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
    return render(request, 'form.html', {'form': form, 'title': 'New Invoice'})


@role_required('admin')
@require_POST
def invoice_cancel(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.status = 'cancelled'
    invoice.save()
    messages.success(request, f'Invoice {invoice.invoice_number} cancelled.')
    return redirect('invoice_detail', pk=pk)


@role_required('finance', 'admin')
@require_POST
def invoice_from_order(request, order_pk):
    """Auto-issue an invoice for a service order"""
    order = get_object_or_404(ServiceOrder.objects.select_related('customer', 'plan'), pk=order_pk)
    invoice = Invoice.objects.create(
        customer=order.customer, plan=order.plan,
        amount=order.plan.price, due_date=timezone.localdate() + timedelta(days=7),
        order=order, created_by=request.user,
    )
    messages.success(request, f'Invoice {invoice.invoice_number} issued for this service.')
    return redirect('invoice_detail', pk=invoice.pk)
