from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mtlsdemo.models import DataLog
from serializers import DataLogSubmitSerializer


class DataLogApiView(APIView):
    def post(self, request):
        serializer = DataLogSubmitSerializer(data=request.data)

        if not serializer.is_valid():
            Response({
                'success': False,
                'error': 'Invalid data',
                'details': serializer.errors
            },
                status=status.HTTP_400_BAD_REQUEST
            )

        DataLog.objects.create(
            level=serializer.validated_data['level'],
            message=serializer.validated_data.get('message', ''),
        )

        return Response({
            'success': True,
            'message': 'Log entry created successfully',
        },
            status=status.HTTP_201_CREATED
        )
