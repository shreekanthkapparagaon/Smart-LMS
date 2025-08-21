# from django.shortcuts import render
from django.http import JsonResponse
from entries.models import LogEntries
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.utils import timezone
from users.models import CustomUser

@csrf_exempt  # Only for testing; use CSRF protection in production
def log_visit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_email = data.get('user')

            userInst = CustomUser.objects.filter(email=user_email).first()
            if not userInst:
                return JsonResponse({'message': 'User not found'}, status=404)

            # Check for an active log (entered but not exited)
            active_log = LogEntries.objects.filter(user=userInst, exited_at__isnull=True).order_by('-entered_at').first()

            if active_log:
                # Update exit time
                active_log.exited_at = timezone.now()
                active_log.save()
                return JsonResponse({
                    'message': 'Exit time recorded',
                    'log_id': active_log.id,
                    'entered_at': active_log.entered_at,
                    'exited_at': active_log.exited_at
                })
            else:
                # Create new entry log
                new_log = LogEntries.objects.create(
                    user=userInst,
                    entered_at=timezone.now()
                )
                return JsonResponse({
                    'message': 'Visit started',
                    'log_id': new_log.id,
                    'entered_at': new_log.entered_at
                })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

def log_entries(request):
    data=[]
    if request.method == 'GET':
        data = list(LogEntries.objects.all().values())
    return JsonResponse({"data":data})
