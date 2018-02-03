from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

import reversion
import datetime


def upload_to(instance, filename):
    return 'users/images/%s/%s' % (instance.user.id, filename)


@reversion.register()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)
    body_fat = models.IntegerField(default=0)
    gender = models.CharField(max_length=20, default='Male')
    about = models.TextField(max_length=255, default='About')
    avatar = models.ImageField(upload_to=upload_to, blank=True)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username


@reversion.register()
class BodyStatTracking(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    height = models.PositiveIntegerField(null=False, default=0)
    bmi = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2)
    weight = models.DecimalField(blank=True, null=False, max_digits=4, decimal_places=1, default=0)
    body_fat = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)

    def __str__(self):
        return self.profile.user.username

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.bmi = (self.weight / (self.height**2)) * 703 if self.weight != 0 and self.height != 0 else 0
        super(BodyStatTracking, self).save()


class Exercises(models.Model):
    exercise_name = models.CharField(max_length=60, unique=True)
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
    lifting_weight = models.IntegerField(null=True, blank=True)
    sets = models.IntegerField()
    reps = models.IntegerField()
    notes = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=3)

    def __str__(self):
        return self.exercise_name


class MaxLiftTracking(models.Model):
    one_rep = 'One Rep Max'
    three_rep = 'Three Rep Max'

    TYPES = ((one_rep, '1 Rep Max'), (three_rep, '3 Rep Max'))

    profile = models.ForeignKey(Profile)
    exercise = models.ForeignKey(Exercises)
    created = models.DateTimeField(auto_now_add=True)
    max_type = models.CharField(max_length=32, choices=TYPES)
    weight = models.PositiveIntegerField()

    def __str__(self):
        return self.exercise.exercise_name


@reversion.register()
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


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def create_body_stat_tracking(sender, instance, created, **kwargs):
    if created:
        BodyStatTracking.objects.create(profile=instance)


