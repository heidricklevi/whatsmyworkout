from django.contrib import admin
from .models import Profile, Workout, Exercise, Exercises, BodyStatTracking, MaxLiftTracking
from django.contrib.auth.models import User
from reversion.admin import VersionAdmin


class MaxLiftTrackingAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'id')

class SubscriberAdmin(admin.ModelAdmin):
    pass


# # class SubscriberInline(admin.StackedInline):
#     model = Subscriber
#     fk_name = 'user_from'


class ProfileAdmin(VersionAdmin):
    # inlines = [SubscriberInline, ]
    readonly_fields = ('id', )


class UserAdmin(admin.ModelAdmin):
    pass


class BodyStatTrackingAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )


class WorkoutAdmin(VersionAdmin):
    list_display = ('user', 'title', 'target_muscle', 'training_type')
    prepopulated_fields = {'slug': ('date_for_completion', 'title',)}


class ExercisesAdmin(admin.ModelAdmin):
    pass


class ExerciseAdmin(admin.ModelAdmin):
    pass


# admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(MaxLiftTracking, MaxLiftTrackingAdmin)
admin.site.register(BodyStatTracking, BodyStatTrackingAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Exercises, ExerciseAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



