from django.contrib import admin
from .models import Profile, Workout, Exercise, Exercises
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class ProfileAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'target_muscle', 'training_type')
    prepopulated_fields = {'slug': ('date_for_completion', 'title',)}


class ExercisesAdmin(admin.ModelAdmin):
    pass


class ExerciseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Exercises, ExerciseAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



