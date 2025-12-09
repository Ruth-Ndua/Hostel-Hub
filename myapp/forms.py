from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Payment, MaintenanceRequest, TenantProfile, AdminProfile, User, Room, Announcement

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='tenant'
    )
    # In forms.py, update the __init__ method of SignUpForm
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'] = forms.ModelChoiceField(
        queryset=Room.objects.filter(status='vacant'),
        required=False,
        empty_label="Select a room",
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['move_in_date'] = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        )
        self.fields['phone'].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2', 'user_type')

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        room = cleaned_data.get('room')
        move_in_date = cleaned_data.get('move_in_date')

        if user_type == 'tenant' and not room:
            self.add_error('room', 'Tenants must select a room')
        if user_type == 'tenant' and not move_in_date:
            self.add_error('move_in_date', 'Move-in date is required for tenants')
        if user_type != 'tenant' and (room or move_in_date):
            cleaned_data['room'] = None
            cleaned_data['move_in_date'] = None

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        user.phone = self.cleaned_data['phone']
        
        # Set is_staff for admin users
        if user.user_type == 'admin':
            user.is_staff = True
            user.is_superuser = True

        if commit:
            user.save()  # This triggers the signal to create the profile

        # Now fill the TenantProfile fields for tenant users
        if user.user_type == 'tenant':
            profile = user.tenantprofile  # created by the signal
            room = self.cleaned_data.get('room')
            if room:
                profile.room = room
                room.status = 'occupied'
                room.save()
            profile.move_in_date = self.cleaned_data['move_in_date']
            profile.save()

        return user




class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount','mpesa_code','month','status')

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['category', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Describe the issue in detail...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the choices from the model's category field
        if 'category' in self.fields:
            self.fields['category'].choices = self.get_category_choices()
    
    def get_category_choices(self):
        """Get category choices from the model's CATEGORY_CHOICES"""
        from .models import MaintenanceRequest
        return MaintenanceRequest.CATEGORY_CHOICES

class MaintenanceStatusForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter announcement title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter announcement details'})
        }