from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=64)
    category = forms.ChoiceField(
        choices=[('none', 'Empty'), ('phones', 'Phones'), ('laptops', 'Laptops'), ('monitors', 'Monitors'),
                 ('tv', 'TV')], label='Category', required=False)


class CommentForm(forms.Form):
    name = forms.CharField(label='Name', max_length=32, widget=forms.TextInput(attrs={'placeholder': 'e.g. John Doe'}))
    email = forms.EmailField(label='Email', max_length=256, widget=forms.EmailInput(attrs={'placeholder': 'email@domain.com'}))
    comment = forms.CharField(label='Comment', widget=forms.Textarea(attrs={'placeholder': 'Type your comment here'}))

