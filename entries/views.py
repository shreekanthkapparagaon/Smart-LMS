# from django.shortcuts import render
from entries.models import LogEntries
from datetime import datetime
from users.models import CustomUser

# restframework views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import logSerializer
from rest_framework.views import APIView

@api_view(['GET'])
def log_entries(request):
    data = list(LogEntries.objects.all().values())
    return Response({"data":data},status=status.HTTP_200_OK)
@api_view(['POST'])
def log_visit(request):
    if 'id' in request.data:
        try:
            userInst = CustomUser.objects.filter(id = request.data['id']).first()
            if not userInst:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Check for an active log (entered but not exited)
            active_log = LogEntries.objects.filter(user=userInst, exited_at__isnull=True).order_by('-entered_at').first()

            if active_log:
                # Update exit time
                active_log.exited_at = datetime.now()
                active_log.save()
                return Response({
                    'message': f'Exit time recorded for {userInst.email}',
                    'log_id': active_log.id,
                    'entered_at': active_log.entered_at,
                    'exited_at': active_log.exited_at
                },status=status.HTTP_200_OK)
            else:
                # Create new entry log
                new_log = LogEntries.objects.create(
                    user=userInst,
                    entered_at=datetime.now()
                )
                return Response({
                    'message': f'Visit started for {userInst.email}',
                    'log_id': new_log.id,
                    'entered_at': new_log.entered_at
                },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message':'post request require "id"...'},status=status.HTTP_400_BAD_REQUEST)
# class VisitCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         if 'user' in request.data:
#             userInst = CustomUser.objects.filter(id = request.data['user']).first()
#             if not userInst:
#                 return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#         # Check for an active log (entered but not exited)
#         active_log = LogEntries.objects.filter(user=userInst, exited_at__isnull=True).order_by('-entered_at').first()

#         if active_log:
#             # Update exit time
#             active_log.exited_at = datetime.now()
#             active_log.save()
#             return Response({
#                 'message': 'Exit time recorded',
#                 'log_id': active_log.id,
#                 'entered_at': active_log.entered_at,
#                 'exited_at': active_log.exited_at
#             },status=status.HTTP_200_OK)
#         else:
#             # Create new entry log
#             new_log = LogEntries.objects.create(
#                 user=userInst,
#                 entered_at=datetime.now()
#             )
#             return Response({
#                 'message': 'Visit started',
#                 'log_id': new_log.id,
#                 'entered_at': new_log.entered_at
#             },status=status.HTTP_201_CREATED)