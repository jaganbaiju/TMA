from. models import User

def current_user(request):
    
    return dict(user=request.user)

def all_users(request):
    users = User.objects.all().filter(role="user")

    return dict(users=users)