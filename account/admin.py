from django.contrib import admin
from .models import Profile, Workout, Exercise, Exercises
from django.contrib.auth.models import User
from reversion.admin import VersionAdmin


class SubscriberAdmin(admin.ModelAdmin):
    pass


# # class SubscriberInline(admin.StackedInline):
#     model = Subscriber
#     fk_name = 'user_from'


class ProfileAdmin(VersionAdmin):
    # inlines = [SubscriberInline, ]
    pass

class UserAdmin(admin.ModelAdmin):
    pass


class WorkoutAdmin(VersionAdmin):
    list_display = ('user', 'title', 'target_muscle', 'training_type')
    prepopulated_fields = {'slug': ('date_for_completion', 'title',)}


class ExercisesAdmin(admin.ModelAdmin):
    pass


class ExerciseAdmin(admin.ModelAdmin):
    pass


# admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Exercises, ExerciseAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



