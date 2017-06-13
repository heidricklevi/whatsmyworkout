import pprint

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework import pagination
from rest_framework.response import Response


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    avatar = serializers.ImageField(source='profile.avatar', default='/media/levi_heidrick.jpg')
    gender = serializers.CharField(source='profile.gender', default='Male')
    body_fat = serializers.IntegerField(source='profile.body_fat', default=12)
    about = serializers.CharField(source='profile.about', default='This is my About')
    weight = serializers.IntegerField(source='profile.weight', default=143)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'date_joined', 'last_login',
                  'first_name', 'last_name', 'password',
                  'avatar', 'weight', 'gender', 'body_fat', 'about')

        read_only_fields = ('date_joined', 'last_login')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)
        self.create_or_update_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        instance.profile.avatar = validated_data.get('avatar', validated_data['profile']['avatar'])
        instance.profile.body_fat = validated_data.get('body_fat', validated_data['profile']['body_fat'])
        instance.profile.about = validated_data.get('about', validated_data['profile']['about'])
        instance.profile.weight = validated_data.get('weight', validated_data['profile']['weight'])

        instance.save()

        password = validated_data.get('password', None)

        profile_data = validated_data.pop('profile', None)

        if password:
            instance.set_password(password)
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)
        self.create_or_update_profile(instance, profile_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def create_or_update_profile(self, user, profile_data):
        profile, created = Profile.objects.get_or_create(user=user, defaults=profile_data)
        if not created and profile_data is not None:
            super(UserSerializer, self).update(profile, profile_data)


class ExercisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = ('id', 'exercise_name', 'target_muscle', 'exercise_rating', 'start_exercise_image',
                  'during_exercise_image', 'exercise_link')


class ExerciseSerializer(serializers.ModelSerializer):
    exercises = ExercisesSerializer(allow_null=True)
    workout_name = serializers.CharField(max_length=255, write_only=True)  # not a field of the model

    class Meta:
        model = Exercise
        fields = ('id', 'exercise_name', 'sets', 'reps', 'notes', 'user', 'exercises', 'workout_name')

    def create(self, validated_data):
        self.associate_exercises(validated_data)
        workout_name = validated_data.pop('workout_name')
        workout = Workout.objects.get(title=workout_name)

        exercise = super(ExerciseSerializer, self).create(validated_data)

        workout.exercises.add(exercise)
        workout.save()

        return exercise

    def update(self, instance, validated_data):
        self.associate_exercises(validated_data)
        return super(ExerciseSerializer, self).update(instance, validated_data)

    def associate_exercises(self, validated_data):
        exercises = validated_data.pop('exercises')

        if not Exercises.objects.filter(exercise_name=exercises['exercise_name']).exists():
            return

        exercises_instance = Exercises.objects.get(exercise_name=exercises['exercise_name'])
        validated_data['exercises'] = exercises_instance


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Workout
        fields = '__all__'

    def create(self, validated_data):
        self.create_or_update(validated_data)
        return super(WorkoutSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        self.create_or_update(validated_data)
        return super(WorkoutSerializer, self).update(instance, validated_data)

    def create_or_update(self, validated_data):
        exercises = validated_data.pop('exercises')
        print(exercises)

        for exercise in exercises:
            Exercise.objects.create(**exercise)








