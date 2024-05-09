from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=64)
    category = forms.ChoiceField(
        choices=[('none', 'Empty'), ('phones', 'Phones'), ('laptops', 'Laptops'), ('monitors', 'Monitors'),
                 ('tv', 'TV')], label='Category', required=False)
