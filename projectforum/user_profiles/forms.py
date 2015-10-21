from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    firstname = forms.CharField(label="First Name", max_length=30)
    lastname = forms.CharField(label="Last Name", max_length=30)
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
