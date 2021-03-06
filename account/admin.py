from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from reversion.admin import VersionAdmin


class MaxLiftTrackingAdmin(admin.ModelAdmin):
    readonly_fields = ('target_muscle', 'created', 'id')
    list_display = ('get_username', 'get_exercise_name', 'created', 'target_muscle')

    def get_exercise_name(self, obj):
        return obj.exercise.exercise_name

    get_exercise_name.admin_order_field = 'exercise__exercise_name'
    get_exercise_name.short_description = 'Exercise Name'

    def get_username(self, obj):
        return obj.profile.user.username

    get_username.admin_order_field = 'profile__user__username'
    get_username.short_description = 'User'


class SubscriberAdmin(admin.ModelAdmin):
    pass


class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'expiry')


class AccountSettingsAdmin(admin.ModelAdmin):
    pass

# # class SubscriberInline(admin.StackedInline):
#     model = Subscriber
#     fk_name = 'user_from'


class ProfileAdmin(VersionAdmin):
    # inlines = [SubscriberInline, ]
    readonly_fields = ('id', )


class UserAdmin(admin.ModelAdmin):
    pass


class WorkoutNotificationSettingsAdmin(admin.ModelAdmin):
    pass


class FriendSubscriptionSettingsAdmin(admin.ModelAdmin):
    pass


class TargetMusclesAdmin(admin.ModelAdmin):
    pass


class BodyStatTrackingAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'username')


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'target_muscle', 'training_type')
    prepopulated_fields = {'slug': ('date_for_completion', 'title',)}
    empty_value_display = '-empty-'


class ExercisesAdmin(admin.ModelAdmin):
    list_display = ('exercise_name', 'target_muscle')


class ExerciseAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'id', )


# admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(TargetMuscles, TargetMusclesAdmin)
admin.site.register(PasswordReset, PasswordResetAdmin)
admin.site.register(AccountSettings, AccountSettingsAdmin)
admin.site.register(WorkoutNotificationSettings, WorkoutNotificationSettingsAdmin)
admin.site.register(FriendSubscriptionSettings, FriendSubscriptionSettingsAdmin)
admin.site.register(MaxLiftTracking, MaxLiftTrackingAdmin)
admin.site.register(BodyStatTracking, BodyStatTrackingAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Exercises, ExercisesAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



