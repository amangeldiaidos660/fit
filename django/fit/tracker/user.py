from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from torch import layout
from .models import User, WorkoutType, Record
from datetime import datetime


def get_progress(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    if not start_date or not end_date:
        return JsonResponse({'status': 'error', 'message': 'Start and end dates are required'}, status=400)

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid date format'}, status=400)

    records = Record.objects.filter(workout_date__range=[start_date, end_date])

    record_data = []
    for record in records:
        record_data.append({
            'date': record.workout_date.strftime('%Y-%m-%d'),
            'data': record.workout_data  
        })

    return JsonResponse({'status': 'success', 'records': record_data})





def get_workout_types(request):
    try:
        workout_types = WorkoutType.objects.all()
        types_data = [{'id': workout.id, 'name': workout.name} for workout in workout_types]
        return JsonResponse({'status': 'success', 'workout_types': types_data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def get_user_data(request):
    user_id = request.session.get('user_id')  
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'User not logged in'}, status=403)

    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({
            'status': 'success',
            'user': {
                'email': user.email,
                'login': user.login,
                'name': user.name,
            }
        })
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)


@csrf_exempt
def logout_view(request):
    layout(request)
    request.session.flush()
    return JsonResponse({'status': 'success', 'message': 'Logged out successfully'})
