from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from .permissions import *
from rest_framework import generics
from django.core.mail import EmailMultiAlternatives
from anymail.message import attach_inline_image_file
from django.template.loader import get_template, render_to_string
from django.template import Context
from rest_framework.response import Response
from whatsmyworkout.config import *
import json


class ExercisesList(generics.ListAPIView):

    permission_classes = [IsAdminOrReadOnly, ]
    queryset = Exercises.objects.order_by('target_muscle')
    serializer_class = ExercisesSerializer


class ExercisesViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = ExercisesSerializer

    def get_queryset(self):
        return Exercises.objects.all()


class WorkoutList(APIView):

    permission_classes = [IsAdminOrAccountOwner, ]

    def get(self, request, format=None):
        print(request.user)
        if not request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = Workout.objects.all().filter(user=request.user).order_by('-date_for_completion')

        serializer = WorkoutSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAccountOwner, ]
    serializer_class = WorkoutSerializer

    def get_queryset(self, format=None):
        queryset = Workout.objects.all()
        month = self.request.query_params.get('month', None)
        recent = self.request.query_params.get('recent', None)

        if month is not None:
            queryset = queryset.filter(user=self.request.user).filter(date_for_completion__month=month)
        elif recent is not None:
            recent = int(recent)
            queryset = queryset.filter(user=self.request.user).order_by('-date_for_completion')[:recent]
        else:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class ExerciseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAccountOwner, ]
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        return Exercise.objects.all().filter(user=self.request.user)


class UserLogin(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        json_content = json.loads(str(request.body.decode('utf-8')))

        username = json_content['username']
        password = json_content['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                print('logging in')
                login(request, user)
                serialized = UserSerializer(user)
                return Response(serialized.data)
            else:
                return Response(status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUser(APIView):
    permission_classes = [permissions.AllowAny]
    authorized_signup = auth_signup_list

    def post(self, request):
        user_data = json.loads(str(request.body.decode('utf-8')))
        serialized = UserSerializer(data=user_data)

        if serialized.is_valid():
            if user_data['email'] not in self.authorized_signup:
                return Response(serialized.data, status=status.HTTP_403_FORBIDDEN)

            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class SendWorkoutEmail(APIView):
    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]

    def post(self, request):
        image = request.data.pop('workout_image')
        to_email = request.data.pop('to')
        serialized = WorkoutSerializer(data=request.data)

        exercises = {}

        if serialized.is_valid():
            payload = {
                'date_for_completion': serialized.data['date_for_completion'],
                'target_muscle': serialized.data['target_muscle'],
                'title': serialized.data['title'],
                'training_type': serialized.data['training_type'],
                'exercises': serialized.data['exercises']
            }

            text_email = get_template('workoutemail.txt')

            d = Context({'payload': payload, 'username': request.user})
            text_content = text_email.render(d)

            message = EmailMultiAlternatives("Workout For The Day", text_content,
                                             from_email=email_config['DEFAULT_FROM_EMAIL'], to=[to_email])
            workout_image = self.set_image(payload['target_muscle'])
            cid = attach_inline_image_file(message, workout_image)
            html_email = render_to_string("workoutemail.html", {'payload': payload, 'username': request.user, 'cid': cid})

            message.attach_alternative(html_email, 'text/html')

            message.send()

            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

    def set_image(self, target_muscle):
        workout_image = None
        account = 'account'
        dev_server = False

        if dev_server:
            account = 'whatsmyworkout/account'

        if target_muscle == 'Chest':
            workout_image = account + '/static/img/chest-muscle.jpg'
        elif target_muscle == 'Biceps':
            workout_image = account + '/static/img/biceps.jpg'
        elif target_muscle == 'Triceps':
            workout_image = account + '/static/img/triceps.jpg'
        elif target_muscle == 'Quads':
            workout_image = account + '/static/img/quads.jpg'
        elif target_muscle == 'Traps':
            workout_image = account + '/static/img/traps.jpg'
        elif target_muscle == 'Lats':
            workout_image = account + '/static/img/lats.jpg'
        elif target_muscle == 'Forearm':
            workout_image = account + '/static/img/forearm.jpg'
        elif target_muscle == 'Calves':
            workout_image = account + '/static/img/calf.jpg'
        elif target_muscle == 'Abdominal':
            workout_image = account + '/static/img/abs.jpg'

        return workout_image


def index(request):
    return render(request, 'index.html')
