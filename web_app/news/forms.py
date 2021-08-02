from django import forms


class CommentsForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea)
    website = forms.URLField()
