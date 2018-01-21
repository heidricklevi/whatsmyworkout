from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from .models import *
from friendship.models import Friend, Follow


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    avatar = serializers.ImageField(source='profile.avatar', required=False)
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
        user.set_password(validated_data['password'])
        self.create_or_update_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        avatar = profile_data.get('avatar', None)

        if avatar is not None:
            instance.profile.avatar = profile_data.get('avatar', None)

        instance.profile.body_fat = profile_data.get('body_fat', None)
        instance.profile.about = profile_data.get('about', None)
        instance.profile.weight = profile_data.get('weight', None)

        instance.save()

        password = validated_data.get('password', None)

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


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class ExercisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = ('id', 'exercise_name', 'target_muscle', 'exercise_rating', 'start_exercise_image',
                  'during_exercise_image', 'exercise_link')


class ExerciseSerializer(serializers.ModelSerializer):
    exercises = ExercisesSerializer(allow_null=True)
    workout_id = serializers.CharField(max_length=255, write_only=True)  # not a field of the model

    class Meta:
        model = Exercise
        fields = ('id', 'exercise_name', 'sets', 'reps', 'lifting_weight', 'notes', 'user', 'exercises', 'workout_id')

    def create(self, validated_data):
        self.associate_exercises(validated_data)
        workout_id = validated_data.pop('workout_id')
        workout = Workout.objects.get(id=workout_id)

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
    exercises = ExerciseSerializer(many=True, allow_null=True, required=False)
    workout_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Workout
        fields = ('id', 'user', 'exercises', 'date_for_completion', 'title', 'workout_image', 'slug', 'target_muscle', 'training_type')

    def create(self, validated_data):
        self.create_or_update(validated_data)
        self.set_workout_image(validated_data['target_muscle'], validated_data)
        return super(WorkoutSerializer, self).create(validated_data)

    def update(self, instance, validated_data):

        self.create_or_update(validated_data)
        self.set_workout_image(validated_data['target_muscle'], validated_data)
        return super(WorkoutSerializer, self).update(instance, validated_data)

    def create_or_update(self, validated_data):

        exercises = validated_data.pop('exercises')
        print(exercises)

        for exercise in exercises:
            id = exercise.pop('workout_id')
            Exercise.objects.create(**exercise)

    def set_workout_image(self, target_muscle, validated_data):

        url = ''

        if target_muscle == 'Chest':
            validated_data['workout_image'] = url + 'img/chest-muscle.jpg'
        elif target_muscle == 'Biceps':
            validated_data['workout_image'] = url + 'img/biceps.jpg'
        elif target_muscle == 'Triceps':
            validated_data['workout_image'] = url + 'img/triceps.jpg'
        elif target_muscle == 'Quads':
            validated_data['workout_image'] = url + 'img/quads.jpg'
        elif target_muscle == 'Traps':
            validated_data['workout_image'] = url + 'img/traps.jpg'
        elif target_muscle == 'Lats':
            validated_data['workout_image'] = url + 'img/lats.jpg'
        elif target_muscle == 'Forearm':
            validated_data['workout_image'] = url + 'img/forearm.jpg'
        elif target_muscle == 'Calves':
            validated_data['workout_image'] = url + 'img/calf.jpg'
        elif target_muscle == 'Abdominal':
            validated_data['workout_image'] = url + 'img/abs.jpg'






