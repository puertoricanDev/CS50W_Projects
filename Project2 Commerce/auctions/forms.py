from django import forms

CATEGORY_CHOICES=[
        ('Uncategorized',''),
        ('Home','Home'),
        ('Electronics','Electronics'),
        ('Appliances', 'Appliances'),
        ('Apps & Games', 'Apps & Games'),
        ('Arts, Crafts, & Sewing', 'Arts, Crafts, & Sewing'),
        ('Automotive Parts & Accessories', 'Automotive Parts & Accessories'),
        ('Baby', 'Baby'),
        ('Beauty & Personal Care', 'Beauty & Personal Care'),
        ('Books', 'Books'),
        ('CDs & Vinyl', 'CDs & Vinyl'),
        ('Cell Phones & Accessories', 'Cell Phones & Accessories'),
        ('Clothing, Shoes and Jewelry', 'Clothing, Shoes and Jewelry'),
        ('Collectibles & Fine Art', 'Collectibles & Fine Art'),
        ('Computers', 'Computers'),
        ('Garden & Outdoor', 'Garden & Outdoor'),
        ('Grocery & Gourmet Food', 'Grocery & Gourmet Food'),
        ('Handmade', 'Handmade'),
        ('Health, Household & Baby Care', 'Health, Household & Baby Care'),
        ('Home & Kitchen', 'Home & Kitchen'),
        ('Industrial & Scientific', 'Industrial & Scientific'),
        ('Luggage & Travel Gear', 'Luggage & Travel Gear'),
        ('Movies & TV', 'Movies & TV'),
        ('Musical Instruments', 'Musical Instruments'),
        ('Office Products', 'Office Products'),
        ('Pet Supplies', 'Pet Supplies'),
        ('Premium Beauty', 'Premium Beauty'),
        ('Sports & Outdoors', 'Sports & Outdoors'),
        ('Tools & Home Improvement', 'Tools & Home Improvement'),
        ('Toys & Games', 'Toys & Games'),
        ('Video Games', 'Video Games')

    ]

class NewItemForm(forms.Form):
    title = forms.CharField(label='Item Name', max_length=100, required=True)
    description = forms.CharField(label='Item Description', max_length=250, required=True)
    category = forms.CharField(label="Category ",widget= forms.Select(choices=CATEGORY_CHOICES))
    imgUrl = forms.CharField(label='Image URL', max_length=100, required=False)
    price = forms.DecimalField(decimal_places=2,
         max_digits=8,
         label="Initial Price", 
         required=True
         )

class closedlistingForm(forms.Form):
    closelisting = forms.BooleanField(label="Close auction.")


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)