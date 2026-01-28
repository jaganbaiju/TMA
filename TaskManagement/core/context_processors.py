
def current_user(request):
    return dict(user=request.user)