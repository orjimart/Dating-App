from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import UserProfileForm
from django.utils.dateformat import format as date_format
from cloudinary.uploader import upload
from django.conf import settings  

@login_required
def user_settings(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user) 
        if form.is_valid():
            # Handle the cover photo upload
            cover_photo = request.FILES.get('cover_photo') 

            if cover_photo:
                try:
                    # Upload to Cloudinary
                    result = upload(
                        cover_photo,
                        cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
                        api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
                        api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
                    )
                    # Save the secure URL to the user's profile
                    user.cover_photo = result['secure_url']
                except Exception as e:
                    messages.error(request, f"Error uploading cover photo: {e}")
            
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_settings')
    else:
        form = UserProfileForm(instance=user)

    # Prepare birthday for display in the readable format
    if form.initial.get('birthday'):
        birthday_readable = date_format(form.initial['birthday'], 'F j, Y')
    else:
        birthday_readable = ''

    # Generate initial data from the user instance, using empty strings for None values
    context = {
        'name': form.initial.get('name', '') or '',
        'email': form.initial.get('email', '') or '',
        'description': form.initial.get('description', '') or '',
        'country': form.initial.get('country', '') or '',
        'city': form.initial.get('city', '') or '',
        'birthday': form.initial.get('birthday', '') or '',
        'birthday_readable': birthday_readable,
        'occupation': form.initial.get('occupation', '') or '',
        'marital_status': form.initial.get('marital_status', '') or '',
        'birthplace': form.initial.get('birthplace', '') or '',
        'fav_tv_shows': form.initial.get('fav_tv_shows', '') or '',
        'fav_music_bands': form.initial.get('fav_music_bands', '') or '',
        'fav_movies': form.initial.get('fav_movies', '') or '',
        'fav_games': form.initial.get('fav_games', '') or '',
        'cover_photo': user.cover_photo.url if user.cover_photo else None,  
    }

    return render(request, 'user_settings.html', context)
