from django import forms
from .models import Company, Item


class AddCompForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['is_open']
        widgets = {
            'sn': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{8}',
                'placeholder': 'ex: 12345678'
            }),
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'fullnameHelpBlock'}),
            'shortname': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'shortnameHelpBlock'}),
            'spnsr': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'nameHelpBlock'}),
            'spnsr_shrtname': forms.TextInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{2,4}(-[0-9]{3,4}){2}',
                'placeholder': 'ex: 0912-123-456 or 02-1234-5678',
            }),
            'tel_ext': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@abc.com'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'author': forms.HiddenInput(),
        }


class UpdateCompForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'sn': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{8}',
                'placeholder': 'ex: 12345678'
            }),
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'fullnameHelpBlock'}),
            'shortname': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'shortnameHelpBlock'}),
            'spnsr': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'nameHelpBlock'}),
            'spnsr_shrtname': forms.TextInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{2,4}(-[0-9]{3,4}){2}',
                'placeholder': 'ex: 0912-123-456 or 02-1234-5678',
            }),
            'tel_ext': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@abc.com'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'author': forms.HiddenInput(),
            'is_open': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['is_inquiry', 'is_open', 'is_new']
        widgets = {
            'sn': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cate': forms.Select(attrs={'class': 'form-control'}),
            'specmain': forms.TextInput(attrs={'class': 'form-control'}),
            'specsub': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = '__all__'
        widgets = {
            'sn': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cate': forms.Select(attrs={'class': 'form-control'}),
            'specmain': forms.TextInput(attrs={'class': 'form-control'}),
            'specsub': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_open': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'is_inquiry': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'is_new': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }
