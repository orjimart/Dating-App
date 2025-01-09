# forms.py
from django import forms
from general.models import CustomUser

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'name', 'email', 'description', 'country', 'city', 'birthday',
            'occupation', 'marital_status', 'birthplace', 'fav_tv_shows',
            'fav_music_bands', 'fav_movies', 'fav_games', 'cover_photo'
        ]
        
    cover_photo = forms.ImageField(required=False) 


