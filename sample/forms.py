from django import forms


class WorkRequestForm(forms.Form):
    number_of_items = forms.IntegerField(min_value=1, max_value=100)
