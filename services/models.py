from django.db import models
from django.utils import timezone
from datetime import timedelta


class ServicePlan(models.Model):
    """A sellable service plan: internet, hosting/domain/server, software license"""
    CATEGORY_CHOICES = [
        ('internet', 'Internet (ADSL/TD-LTE)'),
        ('hosting', 'Hosting/Domain/Server'),
        ('license', 'Software License'),
    ]
    DURATION_CHOICES = [
        (1, 'Monthly'),
        (3, 'Quarterly'),
        (6, 'Semi-annual'),
        (12, 'Annual'),
    ]

    name = models.CharField('Plan name', max_length=120)
    category = models.CharField('Category', max_length=20, choices=CATEGORY_CHOICES)
    duration_months = models.PositiveIntegerField('Duration (months)', choices=DURATION_CHOICES, default=1)
    price = models.DecimalField('Price (Toman)', max_digits=12, decimal_places=0)
    specs = models.TextField('Specifications', blank=True, help_text='e.g. 8Mbps, 100GB SSD, license version')
    is_active = models.BooleanField('Active', default=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Service plan'
        verbose_name_plural = 'Service plans'
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} ({self.get_duration_months_display()})'


class Customer(models.Model):
    """Customer (information entered by admin/staff)"""
    full_name = models.CharField('Full name', max_length=150)
    phone = models.CharField('Phone', max_length=15)
    email = models.EmailField('Email', blank=True)
    national_code = models.CharField('National ID', max_length=10, blank=True)
    company = models.CharField('Company', max_length=150, blank=True)
    address = models.TextField('Address', blank=True)
    notes = models.TextField('Notes', blank=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class ServiceOrder(models.Model):
    """A customer's service subscription"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name='Customer')
    plan = models.ForeignKey(ServicePlan, on_delete=models.PROTECT, related_name='orders', verbose_name='Plan')
    start_date = models.DateField('Start date', default=timezone.localdate)
    end_date = models.DateField('End date')
    status = models.CharField('Status', max_length=12, choices=STATUS_CHOICES, default='active')
    account_info = models.CharField('Account info / username', max_length=200, blank=True,
                                    help_text='e.g. ADSL username or registered domain')
    notes = models.TextField('Notes', blank=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Service order'
        verbose_name_plural = 'Service orders'
        ordering = ['-end_date']

    def save(self, *args, **kwargs):
        if not self.end_date and self.start_date and self.plan_id:
            self.end_date = self.start_date + timedelta(days=30 * self.plan.duration_months)
        super().save(*args, **kwargs)

    @property
    def days_remaining(self):
        if self.status != 'active':
            return None
        return (self.end_date - timezone.localdate()).days

    @property
    def is_expiring_soon(self):
        d = self.days_remaining
        return d is not None and d <= 14

    def __str__(self):
        return f'{self.customer} — {self.plan.name}'
