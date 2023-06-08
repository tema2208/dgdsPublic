from django import forms
from multiupload.fields import MultiFileField

class GameUploadForm(forms.Form):
    name = forms.CharField(label='Name')
    genre = forms.CharField(label='Genre')
    description = forms.CharField(label='Description', widget=forms.Textarea)
    platform = forms.CharField(label='Platform')
    poster = forms.FileField(label='Poster')
    images = MultiFileField(label='Images')
    game_file = forms.FileField(label='Game Archive')
    price = forms.FloatField(label='Price')
    wallet_address = forms.CharField(label='Wallet Address')


class TransactionCheckForm(forms.Form):
    transaction_address = forms.CharField(label='Transaction Address')
