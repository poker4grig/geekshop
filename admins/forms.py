from django import forms

from users.forms import UserRegisterForm, UserProfileForm
from mainapp.models import Product, ProductCategory
from users.models import User


class UserAdminRegisterForm(UserRegisterForm):

    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'image')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class UserAdminProfileForm(UserProfileForm):

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False


class ProductAdminEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductAdminEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image' or field_name == 'category':
                field.widget.attrs['class'] = 'form-control'
            elif field_name == 'is_active':
                field.widget.attrs['style'] = 'margin-top: 20px;'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class CategoryAdminEditForm(forms.ModelForm):

    discount = forms.IntegerField(widget=forms.NumberInput(), label='скидка', required=False, min_value=0, max_value=90, initial=0)
    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'discount',)
        # exclude = ()

    def __init__(self, *args, **kwargs):
        super(CategoryAdminEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

