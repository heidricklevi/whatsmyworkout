from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from rest_framework_jwt.views import ObtainJSONWebToken

from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .permissions import *
from .pagination import *
from rest_framework import generics
from django.core.mail import EmailMultiAlternatives
from anymail.message import attach_inline_image_file
from django.template.loader import get_template, render_to_string
from django.template import Context
from rest_framework.response import Response
from whatsmyworkout.config import *
from reversion.models import Version
from friendship.models import *
from friendship.exceptions import *
from django.utils import timezone
import json
from datetime import date
import string
import random
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class ConfirmPasswordReset(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        json_content = json.loads(str(request.body.decode('utf-8')))
        username = json_content['username']
        token = json_content['token']
        password = json_content['password']

        try:
            user = User.objects.get(username=username)
        except:
            user = None
            return Response({'status': 'Username not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pass_obj = PasswordReset.objects.get(token=token)
        except:
            return Response({'status': 'Token Does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if user and pass_obj:
            if timezone.now() < pass_obj.expiry and pass_obj.used is False:
                user.set_password(password)
                pass_obj.used = True
                pass_obj.save()
                user.save()
                return Response({'status': 'Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'Status': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Status': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordReset(APIView):
    permission_classes = [permissions.AllowAny]

    def random_password(self):
        size = random.randint(8, 21)
        token = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(size))
        return token

    def post(self, request, format=None):
        json_content = json.loads(str(request.body.decode('utf-8')))
        email = json_content['email']

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            user = None

        if user:

            expiry = datetime.datetime.now()+ datetime.timedelta(days=1)
            token = self.random_password()
            pass_reset = PasswordReset.objects.get_or_create(user=user, token=token, expiry=expiry)

            message = EmailMultiAlternatives("Requested Password Reset",
                                             from_email=email_config['DEFAULT_FROM_EMAIL'], to=[email])
            html_email = render_to_string("password_reset_email.html",
                                          {'username': user.username, 'password': token})
            message.attach_alternative(html_email, 'text/html')
            message.send()

        print(user)
        return Response({'status': 'Thank you. If an account with that email address exists, you will receive reset instructions via email. '},
                        status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class LoginJWT(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data['username'])
            user.last_login = timezone.now()
            user.save()
        return response


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FriendProfileUserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = ListFriendSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """

        if self.action == 'retrieve':
            permission_classes = [IsAccountOwnerOrIsFriend, permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]


class UserSearchListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = ListFriendSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'email')


class FriendSearchListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAccountOwnerOrIsFriend]

    serializer_class = FriendSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('from_user__username',)

    def get_queryset(self):
        return Friend.objects.filter(to_user=self.request.user)


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


class BodyStatTrackingViewSet(viewsets.ModelViewSet):

    serializer_class = BodyStatSerializer
    pagination_class = CustomExercisesPagination
    lookup_field = 'username'

    def get_queryset(self):
        queryset = BodyStatTracking.objects.filter(profile__user=self.request.user).order_by('-created')
        return queryset

    def retrieve(self, request, *args, **kwargs):

        queryset = BodyStatTracking.objects.filter(username=kwargs['username']).last()

        self.check_object_permissions(self.request, kwargs['username'])
        serialized = BodyStatSerializer(queryset)
        return Response(serialized.data)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """

        if self.action == 'list':
            permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]
        else:
            permission_classes = [IsAccountOwnerOrIsFriend, permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        to_be_removed = self.request.query_params.get('id', None)

        if to_be_removed is not None:
            body_stat = BodyStatTracking.objects.get(pk=to_be_removed)
            removed = body_stat.delete()

            if removed:
                return Response({"status": "Successfully Deleted"}, status=status.HTTP_200_OK)

        return Response({"status": "Error Deleting"}, status=status.HTTP_400_BAD_REQUEST)


class MaxLiftTrackingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]
    serializer_class = MaxLiftSerializer
    pagination_class = CustomExercisesPagination

    def get_queryset(self):
        target_muscle = self.request.query_params.get('target_muscle', None)
        max_type = self.request.query_params.get('max_type', None)
        exercise_name = self.request.query_params.get('exercise_name', None)
        friend = self.request.query_params.get('friend', None)
        latest = self.request.query_params.get('latest', None)
        earliest = self.request.query_params.get('earliest', None)
        max = self.request.query_params.get('max', None)

        q = MaxLiftTracking.objects.filter(profile__user=self.request.user)

        if friend:
            q = MaxLiftTracking.objects.filter(profile__user__username=friend)

        if target_muscle is not None and not max_type:
            q = q.filter(target_muscle=target_muscle).order_by('-created')
        elif max_type is not None and not target_muscle:
            q = q.filter(max_type=max_type).order_by('-created')
        elif max_type is not None and target_muscle is not None:
            q = q.filter(target_muscle=target_muscle).filter(max_type=max_type).order_by("-created")

        if exercise_name and friend:
            q = q.filter(exercise__exercise_name=exercise_name).order_by('created')
        elif exercise_name:
            q = q.filter(exercise__exercise_name=exercise_name)

        if friend and latest:
            q = MaxLiftTracking.objects.filter(profile__user__username=friend).\
                filter(exercise__exercise_name=exercise_name)\
                .filter(max_type=max_type).order_by('-created')[:1]

        if friend and earliest:
            q = MaxLiftTracking.objects.filter(profile__user__username=friend). \
                filter(exercise__exercise_name=exercise_name)\
                .filter(max_type=max_type).order_by('created')[:1]

        if friend and max:
            q = MaxLiftTracking.objects.filter(profile__user__username=friend). \
                filter(exercise__exercise_name=exercise_name)\
                .filter(max_type=max_type).order_by('-weight')[:1]
        elif max:
            q = q.filter(exercise__exercise_name=exercise_name).filter(max_type=max_type).order_by('-weight')[:1]

        return q


class ExercisesList(generics.ListAPIView):

    permission_classes = [IsAdminOrReadOnly, permissions.IsAuthenticated]
    serializer_class = ExercisesSerializer

    def get_queryset(self):
        target_muscle = self.request.query_params.get('target_muscle', None)

        if target_muscle:
            return Exercises.objects.filter(target_muscle=target_muscle)

        return Exercises.objects.all().order_by('target_muscle')


class ExercisesViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdminOrReadOnly, permissions.IsAuthenticated]
    serializer_class = ExercisesSerializer
    pagination_class = CustomExercisesPagination

    def get_queryset(self):
        target_muscle = self.request.query_params.get('target_muscle', None)

        if target_muscle:
            return Exercises.objects.filter(target_muscle=target_muscle)

        return Exercises.objects.all()


class ProfileHistory(APIView):

    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]

    def get(self, request, format=None):

        versions = Version.objects.filter(revision__user=request.user)
        data = []
        for i in versions:
            data.append({
                "revision_user": str(i.revision.user),
                "serialized": i.serialized_data,
                "date_created": i.revision.date_created,
            })

            # print(data)
        # data_serialized = json.dumps(data)
        return Response(data)


class WorkoutList(APIView):

    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]

    def get(self, request, format=None):
        print(request.user)
        if not request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = Workout.objects.all().filter(user=request.user).order_by('-date_for_completion')

        serializer = WorkoutSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def delete(self, request):
        id = request.query_params.get('id', None)
        queryset = Workout.objects.filter(user=request.user.id)

        if id:
            workout = queryset.get(pk=id)
            workout.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Endpoints dealing with follow/friend requests

class FollowView(APIView):
    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        other_user = User.objects.get(pk=request.data['id'])
        qset = Follow.objects.add_follower(request.user, other_user)
        serialized = FollowSerializer(qset)
        return Response(serialized.data, status=201)

    def get(self, request):
        followers = self.request.query_params.get('followers', None)

        if followers is not None:  # show current user followers else show who current user is following
            qset = Follow.objects.filter(followee=request.user)
        else:
            qset = Follow.objects.filter(follower=request.user)

        serializer = FollowSerializer(qset, many=True, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        other_user = User.objects.get(pk=request.data['other_user'])
        is_removed = Follow.objects.remove_follower(request.user, other_user)

        if is_removed:
            return Response({"status": "successfully removed"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Could not be removed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# End endpoints dealing with follow/friend requests


# Endpoints for Friends and Requests Relating to Collaboration

class FriendsViewSet(viewsets.ModelViewSet): # ViewSet for handling friendship requests/rejects & listing friends
    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]
    serializer_class = FriendSerializer

    # queryset to retrieve user friends # get
    def get_queryset(self):

        sent_requests = self.request.query_params.get('sent_requests', None)
        received_requests = self.request.query_params.get('received_requests', None)

        if sent_requests is not None:
            return Friend.objects.sent_requests(user=self.request.user)

        if received_requests is not None:
            return Friend.objects.unread_requests(user=self.request.user)

        return Friend.objects.filter(to_user=self.request.user).order_by('from_user__username')

    # create a friend request v1/friends
    # or respond to received request (accept or reject) based on 'accept' bool val
    def create(self, request, *args, **kwargs):

        is_accept = request.data.pop('accept', None)
        print(is_accept)
        print(request.data)

        # responding to friend request
        if is_accept:
            try:
                new_friendship_request = FriendshipRequest.objects.get(pk=request.data['id'])
                new_friendship_request.accept()

                return Response({'status': 'successfully accepted request'}, status.HTTP_201_CREATED)

            except Exception as e:
                print(e)
                return Response({'status': 'Could not add Friend', 'message': e}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        if is_accept == False:
            try:
                new_friendship_request = FriendshipRequest.objects.get(pk=request.data['id'])
                new_friendship_request.reject()

                return Response({'status': 'successfully rejected request'}, status.HTTP_201_CREATED)

            except Exception as e:
                print(e)
                return Response({'status': 'A problem occurred while rejecting the request'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # sending friend request
        if is_accept is None:
            other_user = User.objects.get(pk=request.data['to_user'])
            try:
                new = Friend.objects.add_friend(
                    request.user,
                    other_user
                )
            except AlreadyExistsError:
                return Response({'status': 'Already Requested'}, status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'successfully sent request'}, status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        to_be_removed = self.request.query_params.get('id', None)
        # other_user = User.objects.get(pk=request.data['to_user'])

        if to_be_removed is not None:
            friend_request = FriendshipRequest.objects.get(pk=to_be_removed)
            removed = friend_request.cancel()

            if removed:
                return Response({"status": "successfully Canceled Friend Request"}, status=status.HTTP_200_OK)

        return Response({"status": "Error Canceling Request"}, status=status.HTTP_400_BAD_REQUEST)


class FriendsView(APIView):  # APIView for deleting friend

    permission_classes = [IsAccountOwnerOrIsFriend, permissions.IsAuthenticated]

    def delete(self, request):
        to_delete_id = self.request.query_params.get('id', None)
        to_user = User.objects.get(id=to_delete_id)

        if to_delete_id is not None:

            removed = Friend.objects.remove_friend(request.user, to_user)

            if removed:
                return Response({'status': 'Removed friend successfully'}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class TargetMusclesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TargetMusclesSerializer
    queryset = TargetMuscles.objects.all()


class WorkoutViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]
    serializer_class = WorkoutSerializer

    def get_queryset(self, format=None):
        queryset = Workout.objects.all().filter(user=self.request.user)

        month = self.request.query_params.get('month', None)
        recent = self.request.query_params.get('recent', None)
        next_workout = self.request.query_params.get('next_workout', None)

        target_muscle = self.request.query_params.get('target_muscle', None)
        exercise_name = self.request.query_params.get('exercise_name', None)
        reps = self.request.query_params.get('reps', None)

        if month is not None:
            queryset = queryset.filter(user=self.request.user).filter(date_for_completion__month=month)
        elif recent is not None:
            recent = int(recent)
            queryset = queryset.filter(user=self.request.user).order_by('-date_for_completion')[:recent]
        elif target_muscle:
            queryset = queryset.filter(target_muscle=target_muscle).distinct()
        elif exercise_name:
            queryset = queryset.filter(exercises__exercise_name=exercise_name).distinct()
        elif reps:
            queryset = queryset.filter(exercises__reps=reps).distinct()
        elif next_workout:
            queryset = queryset.filter(date_for_completion__gte=date.today()).order_by('date_for_completion')[:5]

        else:
            queryset = queryset.filter(user=self.request.user).order_by('-date_for_completion')

        return queryset


class FriendWorkoutViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAccountOwnerOrIsFriend, permissions.IsAuthenticated]
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        friend = self.request.query_params.get('friend', None)

        if friend:
            return Workout.objects.filter(user__username=friend).filter(date_for_completion__lte=date.today()).order_by('-date_for_completion')[:5]

        return None


class AccountSettingsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]
    serializer_class = AccountSettingsSerializer

    def get_queryset(self):
        return AccountSettings.objects.filter(user=self.request.user)


class CopyFriendWorkoutViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAccountOwnerOrIsFriend, permissions.IsAuthenticated]
    serializer_class = CopyExerciseSerializer

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        workout_id = request.data[0]['workout_id']
        workout = Workout.objects.get(id=workout_id)

        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            print(serializer.data)
            print(workout_id)
            print(workout)

            for exercise in serializer.data:
                exercise.pop('user', None)
                exercise.pop('workout_id', None)
                predefined_exercises_to_associate = self.associate_exercises(exercise)
                created_exercise = Exercise.objects.create(**exercise, exercises=predefined_exercises_to_associate)
                workout.exercises.add(created_exercise)

            workout.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def associate_exercises(self, exercise):
        to_associate_exercise = exercise.pop('exercises', None)

        if to_associate_exercise:
            return Exercises.objects.get(exercise_name=to_associate_exercise['exercise_name'])

        return None


class ExerciseViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        queryset = Exercise.objects.filter(user=self.request.user).order_by('created')
        target_muscle = self.request.query_params.get('target_muscle', None)
        exercise_name = self.request.query_params.get('exercise_name', None)
        reps = self.request.query_params.get('reps', None)

        if target_muscle and exercise_name and not reps:
            print('first condition')
            queryset = queryset.filter(target_muscle=target_muscle)\
                .filter(exercise_name=exercise_name)\
                .order_by('created')
        elif reps and target_muscle is not None and exercise_name is not None:
            print('second condition')
            queryset = queryset.filter(target_muscle=target_muscle)\
                .filter(exercise_name=exercise_name)\
                .filter(reps=reps).order_by('created')

        elif target_muscle and not reps and not exercise_name:
            print("third condition")

            queryset = queryset.filter(target_muscle=target_muscle)

        return queryset

    def destroy(self, request, *args, **kwargs):
        delete_id = self.request.query_params.get('id', None)

        deleted = Exercise.objects.get(id=delete_id).delete()

        if deleted:
            return Response({'status': 'Deleted Successfully'})

        return Response(status=status.HTTP_400_BAD_REQUEST)


class SendWorkoutEmail(APIView):
    permission_classes = [IsAdminOrAccountOwner, permissions.IsAuthenticated]

    def post(self, request):
        image = request.data.pop('workout_image')
        to_username = request.data.pop('to')
        to_email = User.objects.get(username=to_username)
        to_email = to_email.email
        serialized = WorkoutSerializer(data=request.data)

        to_user = AccountSettings.objects.get(user__email=to_email)



        exercises = {}

        if serialized.is_valid() and to_user.receive_workouts_from_friends:
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
        elif not to_user.receive_workouts_from_friends:
            return Response({'status': 'Could not be sent. Please make sure your '
                                       'friend has the ability to receive workouts enabled in their settings.'},
                            status=status.HTTP_400_BAD_REQUEST)
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
        elif target_muscle == 'Back':
            workout_image = account + '/static/img/lats.jpg'
        elif target_muscle == 'Forearm':
            workout_image = account + '/static/img/forearm.jpg'
        elif target_muscle == 'Calves':
            workout_image = account + '/static/img/calf.jpg'
        elif target_muscle == 'Abs':
            workout_image = account + '/static/img/abs.jpg'
        elif target_muscle == 'Arms':
            workout_image = account + '/static/img/biceps.jpg'

        #     Need to add default image

        return workout_image


def index(request):
    return render(request, 'index.html')
