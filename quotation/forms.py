from django import forms
from django.core.exceptions import ValidationError

from .models import Company, Item, Inquiry, ItemQuota, Current, Manufacturer, Category
from django.utils import timezone
from .validator import FileValidator, ItemSnValidator
from django.utils.translation import gettext_lazy as _
from .custom.exchange import getrate


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
                'placeholder': 'ex: 0912-123-456 or 02-1234-5678',
            }),
            'tel_ext': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@abc.com', 'required': True}),
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
        exclude = ['is_inquiry', 'is_open']
        widgets = {
            'sn': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cate': forms.Select(attrs={'class': 'form-control'}),
            'mfg': forms.Select(attrs={'class': 'form-control'}),
            'specmain': forms.TextInput(attrs={'class': 'form-control', 'pattern': '^[0-9A-Z]{5,10}'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'remark', 'is_open', 'is_inquiry']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_open': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'is_inquiry': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }


class AddInquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        exclude = ['status', 'is_open']
        widgets = {
            'cate': forms.Select(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'startdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'max': '9999-12-31'}),
            'enddate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'max': '9999-12-31'}),
            'author': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class UpdateQuotaForm(forms.ModelForm):
    class Meta:
        model = ItemQuota
        fields = ['price', 'crnt', 'xchgrt', 'qdate']
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'crnt': forms.Select(attrs={'class': 'form-control'}),
            'qdate': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'max': timezone.now().strftime("%Y-%m-%d"),
            }),
            'xchgrt': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class XlsUploadForm(forms.Form):
    source_code_validator = FileValidator(
        ("xlsx",),
        ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/zip"),
        max_size=1 * 1024 * 1024, )

    source_code_file = forms.FileField(
        required=True,
        max_length=100,
        validators=[source_code_validator],
        label=_("上傳檔案"),
        help_text=_("副檔名為 .xlsx, 檔名不能超過 100 字元"),
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'required': True,
            'accept': '.xlsx',
        })
    )


class Quotaform(forms.Form):
    # prefix = 'oldquota'
    itemsn_validator = ItemSnValidator(
        sn_list=Item.objects.all().values_list('sn', flat=True)
    )
    inquiry_id = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.HiddenInput()
    )
    item_sn = forms.CharField(
        required=True,
        max_length=200,
        validators=[itemsn_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'required': True,
        })
    )
    item_name = forms.CharField(
        required=True,
        max_length=100,
        label=_("品項名稱"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'required': True,
        })
    )
    item_mfg = forms.CharField(
        required=True,
        max_length=50,
        label=_("製造商"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'required': True,
        })
    )
    quota_crnt = forms.CharField(
        required=True,
        max_length=200,
        label=_("幣別"),
        widget=forms.Select(
            choices=Current.objects.all().values_list('name', 'name'),
            attrs={'class': 'form-control'}
        )
    )
    quota_price = forms.DecimalField(
        required=True,
        max_digits=18,
        decimal_places=4,
        label=_("單價"),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'required': True,
            'min': 0,
        })
    )
    quota_time = forms.DateField(
        required=True,
        label=_("報價日期"),
        widget=forms.DateInput(attrs={
            'required': True,
            'class': 'form-control',
            'type': 'date',
            'max': timezone.localtime(timezone.now()).strftime("%Y-%m-%d"),
        })
    )

    def save(self):
        data = self.cleaned_data
        print(data)
        item = Item.objects.get(sn=data['item_sn'])
        itemquota = ItemQuota.objects.get(inquirysn_id=data['inquiry_id'], itemsn=item)
        crnt = Current.objects.get(name__contains=data['quota_crnt'])
        itemquota.crnt = crnt
        rate_data = getrate(crnt.code, data['quota_time'])
        itemquota.xchgrt = rate_data['ex_rate']
        itemquota.price = data['quota_price']
        itemquota.qdate = data['quota_time']
        itemquota.save()


class NewQuotaForm(Quotaform):
    item_sn = None
    item_cate = forms.CharField(
        required=True,
        max_length=10,
        label=_("品項分類"),
        widget=forms.HiddenInput()
    )
    user_id = forms.CharField(
        required=True,
        max_length=10,
        widget=forms.HiddenInput()
    )
    item_spec = forms.CharField(
        required=True,
        max_length=100,
        label=_("規格"),
        widget=forms.TextInput(attrs={
            'required': True,
            'class': 'form-control',
            'pattern': '^[0-9A-Z]{5,10}'
        })
    )
    item_mfgcode = forms.CharField(
        required=True,
        max_length=4,
        label=_("廠商編號"),
        widget=forms.TextInput(attrs={
            'required': True,
            'class': 'form-control',
            'pattern': '^[0-9A-Z]{2}',
        })
    )

    field_order = ['inquiry_id', 'item_cate', 'user_id', 'item_mfg', 'item_mfgcode', 'item_spec',
                   'item_name', 'quota_crnt', 'quota_price', 'quota_time']

    def clean(self):
        cleaned_data = super().clean()
        item_mfg = self.cleaned_data.get('item_mfg')
        item_mfgcode = self.cleaned_data.get('item_mfgcode')
        item_cate = self.cleaned_data.get('item_cate')
        item_spec = self.cleaned_data.get('item_spec')
        mfgnametocode = list(Manufacturer.objects.filter(name__exact=item_mfg).values_list('sn', flat=True))
        mfgcodetoname = list(Manufacturer.objects.filter(sn__exact=item_mfgcode).values_list('name', flat=True))
        speclist = list(
            Item.objects.filter(cate__id=item_cate, mfg__sn=item_mfgcode).values_list('specmain', flat=True))

        if (item_mfg not in mfgcodetoname) or (item_mfgcode not in mfgnametocode):
            raise ValidationError(_('製造商名稱與編號不同。'), code='MfgDataMismatch')

        # if item_spec in speclist:
        #     raise ValidationError(_('規格編號已有。'), code='SpecExist')

    def save(self):
        data = self.cleaned_data
        cate_id = data['item_cate']
        cate_sn = Category.objects.get(id=cate_id).sn
        mfg_sn = data['item_mfgcode']
        mfg_name = data['item_mfg']
        item_spec = data['item_spec']
        item_name = data['item_name']
        inqry_id = data['inquiry_id']
        user_id = data['user_id']
        quota_price = data['quota_price']
        quota_crnt = Current.objects.get(name=data['quota_crnt'])
        quota_time = data['quota_time']
        xchg_rate = getrate(quota_crnt.code, quota_time)['ex_rate']
        item_sn = "{}{}{}".format(cate_sn, mfg_sn, item_spec.zfill(10))

        mfg, mfg_created = Manufacturer.objects.get_or_create(
            cate_id=cate_id,
            sn=mfg_sn,
            name=mfg_name,
        )

        item, item_created = Item.objects.get_or_create(
            sn=item_sn,
            name=item_name,
            cate_id=cate_id,
            mfg=mfg,
            specmain=item_spec,
            author_id=user_id,
        )

        quota, quota_created = ItemQuota.objects.update_or_create(
            itemsn=item,
            inquirysn_id=inqry_id,
            price=quota_price,
            crnt=quota_crnt,
            xchgrt=xchg_rate,
            qdate=quota_time,
            is_new=True,
        )
        print(mfg, mfg_created)
        print(item, item_created)
        print(quota, quota_created)


class AddCateModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['sn', 'name']
        widgets = {
            'sn': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'pattern': '^[0-9A-Z]{2}',
            }),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }


class UpdateCateForm(forms.Form):
    cate_id = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput(),
    )
    name = forms.CharField(
        required=True,
        max_length=20,
        label=_("名稱"),
        widget=forms.TextInput(attrs={
            'required': True,
            'class': 'form-control',
        })
    )

    def save(self):
        data = self.cleaned_data
        cate_id = data['cate_id']
        cate = Category.objects.get(id=cate_id)
        cate.name = data['name']
        cate.save()


class AddMfgModelForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['cate', 'sn', 'name', 'fullname']
        widgets = {
            'sn': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '^[0-9A-Z]{2}',
            }),
            'cate': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UpdateMfgForm(forms.Form):
    mfg_id = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput(),
    )
    name = forms.CharField(
        required=True,
        max_length=20,
        label=_("名稱"),
        widget=forms.TextInput(attrs={
            'required': True,
            'class': 'form-control',
        })
    )
    fullname = forms.CharField(
        max_length=20,
        label=_("名稱"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    def save(self):
        data = self.cleaned_data
        mfg_id = data['mfg_id']
        mfg = Manufacturer.objects.get(id=mfg_id)
        mfg.name = data['name']
        mfg.fullname = data['fullname']
        mfg.save()
