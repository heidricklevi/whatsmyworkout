from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from .forms import UserAccountForm, LoginForm, ProfileForm, UserEditForm, WorkoutForm, ExerciseForm
from django.contrib import messages
from .models import Profile, Workout, Exercise, Exercises
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from .permissions import *
from django.core.paginator import Paginator
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from rest_framework import pagination
from rest_framework import generics
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from anymail.message import attach_inline_image_file
from django.template.loader import get_template, render_to_string
from django.template import Context
import json


#
# with open('..\\..\\Downloads\\bbsorted-beautified.json') as data:
#     json_data = json.load(data)
#     print(json_data)
#     # json_data = json_data['array']
#     for dict in json_data:
#         exercise = Exercises()
#         exercise.exercise_name = dict['exercise_name']
#         exercise.target_muscle = dict['target_muscle']
#         exercise.exercise_rating = dict['exercise_rating']
#         exercise.exercise_link = dict['exercise_link']
#         exercise.start_exercise_image = dict['start_exercise_image']
#         exercise.during_exercise_image = dict['during_exercise_image']
#
#         exercise.save()
#         # time.sleep(3)
#         print('Just Inserted', exercise.target_muscle + '\n' + str(exercise.exercise_rating) + '\n' + exercise.exercise_name)





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
            queryset = Workout.objects.all().filter(user=request.user).order_by('date_for_completion')

        serializer = WorkoutSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer

    def get_queryset(self, format=None):
        return Workout.objects.all().filter(user=self.request.user).order_by('-date_for_completion')[:5]


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

    def post(self, request):
        user_data = json.loads(str(request.body.decode('utf-8')))
        serialized = UserSerializer(data=user_data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class SendWorkoutEmail(APIView):
    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]

    def post(self, request):
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
            print(exercises)
            text_content = text_email.render(d)

            message = EmailMultiAlternatives("Workout For The Day", text_content,
                                             from_email='noreply@whatsmyworkout.co', to=[to_email])
            workout_image = self.set_image(payload['target_muscle'])
            cid = attach_inline_image_file(message, workout_image)
            html_email = render_to_string("workoutemail.html", {'payload': payload, 'username': request.user, 'cid': cid})

            message.attach_alternative(html_email, 'text/html')

            message.send()

            # send_mail('Workout for the day', serialized.data['date_for_completion'], 'admin@whatsmyworkout.co', ["ljheidrick@gmail.com"])
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

    def set_image(self, target_muscle):
        workout_image = None

        if target_muscle == 'Chest':
            workout_image = 'account/static/img/chest-muscle.jpg'
        elif target_muscle == 'Biceps':
            workout_image = 'account/static/img/biceps.jpg'
        elif target_muscle == 'Triceps':
            workout_image = 'account/static/img/triceps.jpg'
        elif target_muscle == 'Quads':
            workout_image = 'account/static/img/quads.jpg'
        elif target_muscle == 'Traps':
            workout_image = 'account/static/img/traps.jpg'
        elif target_muscle == 'Lats':
            workout_image = 'account/static/img/lats.jpg'
        elif target_muscle == 'Forearm':
            workout_image = 'account/static/img/forearm.jpg'
        elif target_muscle == 'Calves':
            workout_image = 'account/static/img/calf.jpg'
        elif target_muscle == 'Abdominal':
            workout_image = 'account/static/img/abs.jpg'

        return workout_image







def create_account(request):
    return render(request, 'accounts/signup.html', {'form': UserAccountForm()})


@login_required
def complete_profile(request):

    if request.method == 'POST':
        user_profile = ProfileForm(data=request.POST, files=request.FILES)

        if user_profile.is_valid():
            user_profile.save()

            return HttpResponseRedirect(reverse('dashboard'))
        else:
            print('failure')

    else:
        user_profile = ProfileForm()
    return render(request, 'dashboard.html', {'user_profile': user_profile})


def signin(request):
    return render(request, 'registration/login.html', {'form': LoginForm()})


def profile(request):
    if request.method == 'POST':
        form = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()

            return redirect('dashboard')

    else:
        form = ProfileForm()


    return render(request, 'registration/profile.html', {'form': form})


def vuetest(request):
    return render(request, "../../whatsmyworkout-vue/index.html")


@login_required
def dashboard(request):
    user_obj = get_object_or_404(Profile, user=request.user)
    print(request.POST)
    if request.method == 'POST':
        form = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        user_form = UserEditForm(instance=request.user, data=request.POST)

        user_form.last_name = request.POST['first_name'].rpartition(' ')[2]

        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()

            return redirect('dashboard')

    else:
        form = ProfileForm()
        user_form = UserEditForm()

    return render(request, 'dashboard.html', {'user_obj': user_obj, 'form': form, 'user_form': user_form})


@login_required
def create_workout(request):
    user_obj = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        user = Workout(user_id=request.user.id)
        workout_form = WorkoutForm(request.POST, instance=user, files=request.FILES)
        exercise_form = ExerciseForm(request.POST)

        if workout_form.is_valid():
            workout_form.save()
            data = {'success': True}
            return JsonResponse(data)

        if exercise_form.is_valid():
            exercise_form.save()

    else:
        workout_form = WorkoutForm()
        exercise_form = ExerciseForm()

    return render(request, 'workout/create-workout.html',
                  {'user_obj': user_obj, 'workout_form': workout_form,
                   'exercise_form': exercise_form})

def index(request):
    return render(request, 'index.html')
