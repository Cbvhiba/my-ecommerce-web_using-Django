from django import forms
from products.models import Product, ProductImages, Catogary, SubCategory
from django.contrib.auth.models import User



class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = SubCategory.objects.none()

        if 'catogary' in self.data:
            try:
                catogary_id = self.data.get('catogary')
                self.fields['subcategory'].queryset = SubCategory.objects.filter(catogary_id=catogary_id).all()
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.uid:
        #     self.fields['subcategory'].queryset = self.instance.catogary.subcategory_set.all()


class ProductImageForm(forms.ModelForm):

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )

    class Meta:
        model = ProductImages
        fields = ['image',]


class CatogaryForm(forms.ModelForm):

    class Meta:
        model = Catogary
        fields = '__all__'


class SubcatogaryForm(forms.ModelForm):

    class Meta:
        model = SubCategory
        fields = '__all__'


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'slug', 'price', 'discount_percent','total_quantity', 'product_desc', 'product_information','tag', 'color_variant', 'size_variant', 'is_featured']