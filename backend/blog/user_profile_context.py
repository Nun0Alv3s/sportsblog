def user_profile(request):
    if request.user.is_authenticated:
        return {
            'user_profile_image': f"/static/{request.user.userprofile.image.url}",
        }
    return {}
