from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('tenant', 'Tenant'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='tenant')
    phone = models.CharField(max_length=20, blank=True)


class Room(models.Model):
    room_number = models.CharField(max_length=20, default=1)
    type = models.CharField(max_length=30, default='Bedsitter')
    rent = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='vacant')  # vacant / occupied

    def __str__(self):
        return f"{self.room_number} ({self.room_type})"

class TenantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    move_in_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s tenant profile"

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hire_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s admin profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Create new profile on first save
    if created:
        if instance.user_type == 'tenant':
            TenantProfile.objects.create(user=instance)
        elif instance.user_type == 'admin':
            AdminProfile.objects.create(user=instance)
    else:
        # Update profile when user is updated
        if instance.user_type == 'tenant':
            instance.tenantprofile.save()
        elif instance.user_type == 'admin':
            instance.adminprofile.save()

class Payment(models.Model):
    tenant = models.ForeignKey(TenantProfile, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    month = models.CharField(max_length=20, blank=True)
    mpesa_code = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, default='pending')  # pending / approved / rejected
    #date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant} - {self.amount} ({self.status})"

class MaintenanceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    CATEGORY_CHOICES = [
        ('Plumbing','Plumbing'),
        ('Electricity','Electricity'),
        ('WiFi','WiFi'),
        ('Other','Other'),
    ]
    tenant = models.ForeignKey(TenantProfile, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, default='pending')  # pending,in-progress,resolved
    admin_notes = models.TextField(blank=True, null=True)
    #date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant} - {self.category} - {self.status}"

    class Meta:
        ordering = ['-id']

class Announcement(models.Model):
    title = models.CharField(max_length=120)
    message = models.TextField()
    #created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

