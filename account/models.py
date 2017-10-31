from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from simple_history.models import HistoricalRecords
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)
    body_fat = models.IntegerField(default=0)
    gender = models.CharField(max_length=20, default='Male')
    about = models.TextField(max_length=255, default='About')
    avatar = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.user.first_name + '\'s Profile' if self.user.first_name else 'No User Name Profile'


class Exercises(models.Model):
    exercise_name = models.CharField(max_length=255)
    exercise_rating = models.CharField(max_length=255, null=True)
    target_muscle = models.CharField(max_length=255)
    exercise_link = models.CharField(max_length=255, null=True)
    start_exercise_image = models.CharField(max_length=255, null=True)
    during_exercise_image = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.exercise_name


class Exercise(models.Model):

    exercises = models.ForeignKey(Exercises, on_delete=models.CASCADE, blank=True, null=True)
    # workout = models.ForeignKey(Workout, on_delete=models.CASCADE, default=1)
    exercise_name = models.CharField(max_length=255, blank=True, null=True)
    weight = models.IntegerField(null=True, blank=True)
    sets = models.IntegerField()
    reps = models.IntegerField()
    notes = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=3)
    history = HistoricalRecords()

    def __str__(self):
        # return self.exercise_name if self.exercises.exercise_name is None else self.exercises.exercise_name
        return self.exercise_name


class Workout(models.Model):

    endurance = 'Endurance'
    strength = 'Strength Training'
    balance = 'Balance Focused'
    flexibility = 'Flexibility Focused'

    traps = 'Traps'
    neck = 'Neck'
    chest = 'Chest'
    biceps = 'Biceps'
    forearm = 'Forearm'
    abs = 'Abdominal'
    quads = 'Quads'
    calves = 'Calves'
    triceps = 'Triceps'
    lats = 'Lats'
    middle_back = 'Middle Back'
    lower_back = 'Lower Back'
    glutes = 'Glutes'
    hamstrings = 'Hamstrings'

    TARGET_MUSCLE = ((traps, 'Traps'), (neck, 'Neck'), (chest, 'Chest'), (biceps, 'Biceps'),
                     (forearm, 'Forearm'), (abs, 'Abdominal'), (quads, 'Quads'), (calves, 'Calves'),
                     (triceps, 'Triceps'), (lats, 'Lats'), (middle_back, 'Middle Back'), (lower_back, 'Lower Back'),
                     (glutes, 'Glutes'), (hamstrings, 'Hamstrings'))

    TRAINING_TYPES = ((endurance, 'Endurance'), (strength, 'Strength Training'), (balance, 'Balance Focused'),
                      (flexibility, 'Flexibility Focused'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()
    exercises = models.ManyToManyField(Exercise)
    date_for_completion = models.DateField(default=datetime.date.today,)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150, )
    workout_image = models.ImageField(blank=True, null=True)

    slug = models.SlugField(max_length=255)
    target_muscle = models.CharField(max_length=255, choices=TARGET_MUSCLE, default=1)
    training_type = models.CharField(max_length=255, choices=TRAINING_TYPES, default=1)




    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('workout', args=[self.date_for_completion,
                                        self.title])







@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()





