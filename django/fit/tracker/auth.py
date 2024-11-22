import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import User  

@csrf_protect 
def register_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

    
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            user = User.objects.create(
                email=email,
                login=username,
                password=hashed_password,
                name=name,
            )
            return JsonResponse({'message': 'Registration successful', 'status': 'success', 'user_id': user.id}, status=201)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}', 'status': 'error'}, status=500)

    return JsonResponse({'message': 'Invalid request method', 'status': 'error'}, status=405)
