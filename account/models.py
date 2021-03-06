from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from friendship.models import Friend
import reversion
import datetime


class PasswordReset(models.Model):
    token = models.CharField(max_length=128, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def upload_to(instance, filename):
    return 'users/images/%s/%s' % (instance.user.id, filename)


# @reversion.register()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    gender = models.CharField(max_length=20, default='Male')
    about = models.TextField(max_length=255, default='About')
    avatar = models.ImageField(upload_to=upload_to, blank=True)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username


# @reversion.register()
class BodyStatTracking(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    height = models.PositiveIntegerField(null=False, default=0)
    bmi = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    weight = models.DecimalField(blank=True, null=False, max_digits=4, decimal_places=1, default=0)
    body_fat = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    username = models.CharField(max_length=255, editable=False)

    def __str__(self):
        return self.profile.user.username

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.username = self.profile.user.username
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

    class Meta:
        ordering = ['target_muscle', 'exercise_name']


class Exercise(models.Model):

    TARGET_MUSCLE = (('Back', 'Back'), ('Arms', 'Arms'),
                     ('Legs', 'Legs'), ('Chest', 'Chest'), ('Biceps', 'Biceps'), ('Triceps', 'Triceps'), ('Shoulders', 'Shoulders'))

    exercises = models.ForeignKey(Exercises, on_delete=models.CASCADE, blank=True, null=True)
    # workout = models.ForeignKey(Workout, on_delete=models.CASCADE, default=1)
    exercise_name = models.CharField(max_length=255, blank=True, null=True)
    lifting_weight = models.IntegerField(null=True, blank=True)
    sets = models.CharField(max_length=28)
    reps = models.CharField(max_length=28)
    notes = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=3)
    target_muscle = models.CharField(max_length=255, choices=TARGET_MUSCLE, default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)

    def __str__(self):
        return str(self.exercise_name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        self.exercise_name = self.exercises.exercise_name if self.exercises else self.exercise_name
        self.target_muscle = self.exercises.target_muscle if self.exercises else self.target_muscle

        super(Exercise, self).save()


class MaxLiftTracking(models.Model):
    one_rep = '1'
    three_rep = '3'

    MAX_TYPES = ((one_rep, '1'), (three_rep, '3'),)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    max_type = models.CharField(max_length=255, choices=MAX_TYPES)
    weight = models.PositiveIntegerField(blank=True, null=True)
    target_muscle = models.CharField(max_length=65, editable=False)
    # max_reps = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.exercise.exercise_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        self.target_muscle = self.exercise.target_muscle
        super(MaxLiftTracking, self).save()

    class Meta:
        ordering = ['target_muscle', '-created']


class TargetMuscles(models.Model):
    traps = 'Traps'
    neck = 'Neck'
    chest = 'Chest'
    biceps = 'Biceps'
    forearm = 'Forearms'
    abs = 'Abs'
    quads = 'Quads'
    calves = 'Calves'
    triceps = 'Triceps'
    lats = 'Lats'
    middle_back = 'Middle Back'
    lower_back = 'Lower Back'
    glutes = 'Glutes'
    hamstrings = 'Hamstrings'

    TARGET_MUSCLE_ = ((traps, 'Traps'), (neck, 'Neck'), (biceps, 'Biceps'),
                     (forearm, 'Forearms'), (abs, 'Abs'), (quads, 'Quads'), (calves, 'Calves'),
                     (triceps, 'Triceps'), (lats, 'Lats'), (middle_back, 'Middle Back'), (lower_back, 'Lower Back'),
                     (glutes, 'Glutes'), (hamstrings, 'Hamstrings'), ('Back', 'Back'), ('Arms', 'Arms'),
                     ('Legs', 'Legs'), (chest, 'Chest'), ('Shoulders', 'Shoulders'))

    name = models.CharField(max_length=2555, choices=TARGET_MUSCLE_, default=1, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


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
    abs = 'Abs'
    quads = 'Quads'
    calves = 'Calves'
    triceps = 'Triceps'
    lats = 'Lats'
    middle_back = 'Middle Back'
    lower_back = 'Lower Back'
    glutes = 'Glutes'
    hamstrings = 'Hamstrings'

    TARGET_MUSCLE = ((traps, 'Traps'), (neck, 'Neck'), (biceps, 'Biceps'),
                     (forearm, 'Forearm'), (abs, 'Abs'), (quads, 'Quads'), (calves, 'Calves'),
                     (triceps, 'Triceps'), (lats, 'Lats'), (middle_back, 'Middle Back'), (lower_back, 'Lower Back'),
                     (glutes, 'Glutes'), (hamstrings, 'Hamstrings'), ('Back', 'Back'), ('Arms', 'Arms'), ('Legs', 'Legs'), (chest, 'Chest'), ('Shoulders', 'Shoulders'))

    TRAINING_TYPES = ((endurance, 'Endurance'), (strength, 'Strength Training'), (balance, 'Balance Focused'),
                      (flexibility, 'Flexibility Focused'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercise)
    date_for_completion = models.DateField(default=datetime.date.today,)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    title = models.CharField(max_length=150, )
    workout_image = models.ImageField(blank=True, null=True)

    muscles = models.ManyToManyField(TargetMuscles, blank=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    target_muscle = models.CharField(max_length=255, choices=TARGET_MUSCLE, default=1)
    training_type = models.CharField(max_length=255, choices=TRAINING_TYPES, default=1)
    completed = models.BooleanField(blank=True, default=False)
    sent_notification = models.BooleanField(default=False, blank=True)

    def __str__(self):

        return 'Workout Name: {}'.format(self.title)


class WorkoutNotificationSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    is_enabled = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)


class FriendSubscriptionSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(Friend, null=True, blank=True, on_delete=models.CASCADE)
    can_receive_content = models.BooleanField(default=False)


class AccountSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workout_notification_settings = models.ForeignKey(WorkoutNotificationSettings, blank=True, null=True, on_delete=models.CASCADE)
    friend_subscription_settings = models.ForeignKey(FriendSubscriptionSettings, blank=True, null=True, on_delete=models.CASCADE)
    friends_can_subscribe = models.BooleanField(default=False)
    receive_workout_notifications = models.BooleanField(default=True)
    receive_workouts_from_friends = models.BooleanField(default=False)

    def __str__(self):
        return "Account Settings for {}".format(self.user.username)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        AccountSettings.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def create_body_stat_tracking(sender, instance, created, **kwargs):
    if created:
        BodyStatTracking.objects.create(profile=instance)


