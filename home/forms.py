from django import forms
from .models import login_register,review

class register(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    class Meta:
        model = login_register
        fields = ['fullname','address','phone_no','email_address','password']
        widgets = {'fullname':forms.TextInput(attrs={'class':'form-control','placeholder':'Full Name'}),
                   'address': forms.TextInput(attrs={'class': 'form-control','placeholder':'Address'}),
                   'phone_no': forms.TextInput(attrs={'class': 'form-control','placeholder':'Phone Number'}),
                   'email_address': forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email Address'}),
                   'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}),
                }
    def clean_confirm_password(self):
        cf = self.cleaned_data.get("confirm_password")
        pa = self.cleaned_data.get("password")
        if cf!=pa:
            raise forms.ValidationError("Confirm password and password does not match")
        return cf
    def clean_email_address(self):
        e = self.cleaned_data.get("email_address")
        checkemail = login_register.objects.filter(email_address=e)
        if len(checkemail)>0:
            raise forms.ValidationError("Either Email address already exists or verification has been sent!")
        return e


class login(forms.ModelForm):
    class Meta:
        model = login_register
        fields = ["email_address","password"]
        widgets = {'email_address':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email Address','name':'lemail','id':'lemail'}),
                   'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'})
                   }
class formcontact(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Subject'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Type Your Text','rows':6}))
class cakeform(forms.Form):
    cakename = forms.CharField(label="What to write on your cake?" , widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Max Characher 30','max-length':'30'}))
    size = forms.IntegerField(label="Size (In Pounds)",widget=forms.NumberInput(attrs={'class':'form-control'}))