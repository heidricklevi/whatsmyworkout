from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from .models import *
from friendship.models import Friend, Follow


class AccountSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSettings
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    avatar = serializers.ImageField(source='profile.avatar', required=False)
    gender = serializers.CharField(source='profile.gender', default='Male')
    about = serializers.CharField(source='profile.about', default='This is my About')
    profile_id = serializers.IntegerField(source='profile.id', required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'date_joined', 'last_login',
                  'first_name', 'last_name', 'password',
                  'avatar', 'gender',  'about', 'profile_id', )

        read_only_fields = ('date_joined', 'last_login', )

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        self.create_or_update_profile(user, profile_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        avatar = profile_data.get('avatar', None)

        if avatar is not None:
            instance.profile.avatar = profile_data.get('avatar', None)

        instance.profile.body_fat = profile_data.get('body_fat', None)
        instance.profile.about = profile_data.get('about', None)
        instance.profile.weight = profile_data.get('weight', None)
        email = validated_data.get('email', None)
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)
        username = validated_data.get('username', None)

        if email:
            instance.email = email

        if first_name:
            instance.first_name = first_name

        if last_name:
            instance.last_name = last_name

        if username:
            instance.username = username

        password = validated_data.get('password', None)
        print(password)
        print(instance)

        if password is not None:
            print(password)
            instance.set_password(password)
            instance.save()

        instance.save()
        update_session_auth_hash(self.context.get('request'), instance)
        self.create_or_update_profile(instance, profile_data)
        return instance

    def create_or_update_profile(self, user, profile_data):
        profile, created = Profile.objects.get_or_create(user=user, defaults=profile_data)
        if not created and profile_data is not None:
            super(UserSerializer, self).update(profile, profile_data)


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class ListFriendSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar', required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'last_login', 'date_joined')


class FriendSerializer(serializers.ModelSerializer):

    from_user = ListFriendSerializer()
    to_user = ListFriendSerializer()

    class Meta:
        model = Friend
        fields = ('id', 'from_user', 'to_user', 'created')


class ExercisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = ('id', 'exercise_name', 'target_muscle', 'exercise_rating', 'start_exercise_image',
                  'during_exercise_image', 'exercise_link')
        extra_kwargs = {
            'exercise_name': {
                'validators': []
            }
        }


class MaxLiftSerializer(serializers.ModelSerializer):

    exercise = ExercisesSerializer()

    class Meta:
        model = MaxLiftTracking
        fields = ('id', 'max_type', 'weight', 'target_muscle', 'created', 'exercise', 'profile', )
        extra_kwargs = {
            'exercise_name': {'validators': []},
        }

    def create(self, validated_data):
        self.associate_predefined_exercise(validated_data)
        print(validated_data)
        return super(MaxLiftSerializer, self).create(validated_data)

    def associate_predefined_exercise(self, validated_data):
        exercise = validated_data.pop('exercise', None)

        if exercise:
            exercise_instance = Exercises.objects.get(exercise_name=exercise['exercise_name'])
            print(exercise_instance)
            validated_data['exercise'] = exercise_instance


class BodyStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyStatTracking
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    exercises = ExercisesSerializer(allow_null=True)
    workout_id = serializers.CharField(max_length=255, write_only=True, allow_null=True)  # not a field of the model

    class Meta:
        model = Exercise
        fields = ('id', 'exercise_name', 'sets', 'reps', 'lifting_weight', 'created', 'notes', 'user', 'exercises', 'workout_id', 'target_muscle')
        extra_kwargs = {
            'lifting_weight':
                {
                    'validators': []
                },
        }

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


class CopyExerciseSerializer(serializers.ModelSerializer):
    exercises = ExercisesSerializer(allow_null=True)
    workout_id = serializers.CharField(max_length=255, write_only=True, allow_null=True)  # not a field of the model

    class Meta:
        model = Exercise
        fields = ('id', 'exercise_name', 'sets', 'reps', 'lifting_weight', 'created', 'notes', 'user', 'exercises', 'workout_id', 'target_muscle')
        extra_kwargs = {
            'lifting_weight':
                {
                    'validators': []
                },
        }

    # def create(self, validated_data):
    #     workout_id = validated_data[0].pop('workout_id', None)
    #     workout = Workout.objects.get(id=workout_id)
    #     print(validated_data)
    #     for exercise in validated_data:
    #         self.associate_exercises(exercise)
    #         exercise_to_add = Exercise.objects.create(**exercise)
    #         workout.exercises.add(exercise_to_add)
    #
    #     return workout
    #
    # def update(self, instance, validated_data):
    #     self.associate_exercises(validated_data)
    #     return super(CopyExerciseSerializer, self).update(instance, validated_data)
    #
    # def associate_exercises(self, validated_data):
    #     exercises = validated_data.pop('exercises')
    #
    #     if not Exercises.objects.filter(exercise_name=exercises['exercise_name']).exists():
    #         return
    #
    #     exercises_instance = Exercises.objects.get(exercise_name=exercises['exercise_name'])
    #     validated_data['exercises'] = exercises_instance


class TargetMusclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetMuscles
        fields = '__all__'


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, allow_null=True, required=False)
    muscles = TargetMusclesSerializer(many=True, allow_null=True, required=False)
    workout_image = serializers.ImageField(required=False, allow_null=True)
    notes = serializers.CharField(max_length=255, source='exercises.notes', required=False, allow_null=True)

    class Meta:
        model = Workout
        fields = ('id', 'user', 'exercises', 'muscles', 'date_for_completion', 'title', 'workout_image',
                  'slug', 'target_muscle', 'training_type', 'completed', 'notes')
        extra_kwargs = {
            'lifting_weight': {'validators': []},
        }

    def create(self, validated_data):
        muscles = validated_data.pop('muscles')

        self.create_or_update(validated_data)
        self.set_workout_image(validated_data['target_muscle'], validated_data)
        instance = super(WorkoutSerializer, self).create(validated_data)
        instance = self.create_associate_tagged_muscles(muscles, instance)
        return instance

    def update(self, instance, validated_data):

        # self.create_or_update(validated_data)
        print(instance.id)
        self.set_workout_image(validated_data['target_muscle'], validated_data)

        print(instance)

        instance.date_for_completion = validated_data.get('date_for_completion', instance.date_for_completion)
        instance.title = validated_data.get('title', instance.title)
        instance.target_muscle = validated_data.get('target_muscle', instance.target_muscle)
        instance.training_type = validated_data.get('training_type', instance.training_type)
        instance.workout_image = validated_data.get('workout_image', None)
        instance.muscles = validated_data.get('muscles', instance.muscles)

        instance.save()

        workout_exercises = validated_data.get('exercises')

        for exercise in workout_exercises:
            e_id = exercise.pop('id', None)
            print(exercise)
            exercises_to_be_added = exercise.pop('exercises', None)

            if e_id:
                exercise_object = Exercise.objects.get(id=e_id)

                if exercises_to_be_added:
                    to_associate = Exercises.objects.get(exercise_name=exercises_to_be_added['exercise_name'])
                    exercise_object.exercises = to_associate

                exercise_object.exercise_name = exercise['exercise_name']
                exercise_object.reps = exercise['reps']
                exercise_object.sets = exercise['sets']
                exercise_object.notes = exercise['notes']
                exercise_object.lifting_weight = exercise['lifting_weight']

                exercise_object.save()

                instance.exercises.add(exercise_object)
            else:
                exercise.pop('workout_id')

                if exercises_to_be_added:

                    to_associate = Exercises.objects.get(exercise_name=exercises_to_be_added['exercise_name'])
                    new_exercise = Exercise.objects.create(**exercise, exercises=to_associate)

                    instance.exercises.add(new_exercise)
                else:
                    new_exercise = Exercise.objects.create(**exercise)
                    instance.exercises.add(new_exercise)

            print(exercises_to_be_added)

        instance.save()

        return instance

    def create_associate_tagged_muscles(self, muscles, workout_instance):
        print(muscles)
        print(workout_instance)

        for muscle in muscles:
            name = muscle.get('name')

            m_obj = TargetMuscles.objects.get(name=name)
            workout_instance.muscles.add(m_obj)

        workout_instance.save()
        return workout_instance



    def create_or_update(self, validated_data):

        exercises = validated_data.pop('exercises')

        for exercise in exercises:
            id = exercise.pop('workout_id', None)
            exercises_to_be_added = exercise.pop('exercises', None)
            print(exercise)

            print(exercises_to_be_added)
            if exercises_to_be_added:
                to_associate = Exercises.objects.get(exercise_name=exercises_to_be_added['exercise_name'])
                Exercise.objects.create(**exercise, exercises=to_associate)
            else:
                Exercise.objects.create(**exercise)

    def set_workout_image(self, target_muscle, validated_data):

        url = ''

        if target_muscle == 'Chest':
            validated_data['workout_image'] = url + 'img/chest-muscle.jpg'
        elif target_muscle == 'Biceps':
            validated_data['workout_image'] = url + 'img/biceps.jpg'
        elif target_muscle == 'Triceps':
            validated_data['workout_image'] = url + 'img/triceps.jpg'
        elif target_muscle == 'Legs':
            validated_data['workout_image'] = url + 'img/quads.jpg'
        elif target_muscle == 'Traps':
            validated_data['workout_image'] = url + 'img/traps.jpg'
        elif target_muscle == 'Back':
            validated_data['workout_image'] = url + 'img/lats.jpg'
        elif target_muscle == 'Forearm':
            validated_data['workout_image'] = url + 'img/forearm.jpg'
        elif target_muscle == 'Calves':
            validated_data['workout_image'] = url + 'img/calf.jpg'
        elif target_muscle == 'Abs':
            validated_data['workout_image'] = url + 'img/abs.jpg'
        elif target_muscle == 'Arms':
            validated_data['workout_image'] = url + 'img/biceps.jpg'






