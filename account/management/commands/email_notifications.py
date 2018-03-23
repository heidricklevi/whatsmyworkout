from django.core.management.base import BaseCommand, CommandError
from account.models import *
from account.serializers import *
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from anymail.message import attach_inline_image_file
from whatsmyworkout.config import *
from datetime import date


class Command(BaseCommand):
    help = 'Send Email Notifications for scheduled workouts'

    def handle(self, *args, **options):
        try:
            workouts = Workout.objects.all().filter(date_for_completion=date.today()).filter(sent_notification=False)
            if workouts:
                for workout in workouts:
                    user_account = AccountSettings.objects.get(user__username=workout.user)

                    if user_account.receive_workout_notifications:
                        self.format_send_email(workout, workout.user)
                        workout.sent_notification = True
                        workout.save()

        except Exception as e:
            print(e.args)

    def format_send_email(self, workout, username):

        to_email = User.objects.get(username=username)
        to_email = to_email.email
        workout = Workout.objects.get(id=workout.id)
        serialized = WorkoutSerializer(workout)

        payload = {
            'date_for_completion': serialized.data['date_for_completion'],
            'target_muscle': serialized.data['target_muscle'],
            'title': serialized.data['title'],
            'training_type': serialized.data['training_type'],
            'exercises': serialized.data['exercises']
        }

        # payload = {
        #         'date_for_completion': workout.date_for_completion,
        #         'target_muscle': workout.target_muscle,
        #         'title': workout.title,
        #         'training_type': workout.training_type,
        #         'exercises': workout.exercises,
        # }

        text_email = render_to_string('workoutemail.txt', {'payload': payload, 'username': username })

        # d = Context({'payload': payload, 'username': username })
        # text_content = text_email.render(d)

        message = EmailMultiAlternatives("Workout For The Day", text_email,
                                             from_email=email_config['DEFAULT_FROM_EMAIL'], to=[to_email])

        workout_image = self.set_image(workout.target_muscle)
        cid = attach_inline_image_file(message, workout_image)
        html_email = render_to_string("workoutemail.html", {'payload': payload, 'username': username, 'cid': cid})

        message.attach_alternative(html_email, 'text/html')
        try:
            message.send()
        except Exception as e:
            print(e.args)

    def set_image(self, target_muscle):
            workout_image = None
            account = 'account'
            dev_server = False

            email_notif_cron = True
            if email_notif_cron:
                account = server_config["workout_notifcations_url"]

            if dev_server:
                account = 'whatsmyworkout/account'

            if target_muscle == 'Chest':
                workout_image = account + '/static/img/chest-muscle.jpg'
            elif target_muscle == 'Biceps':
                workout_image = account + '/static/img/biceps.jpg'
            elif target_muscle == 'Triceps':
                workout_image = account + '/static/img/triceps.jpg'
            elif target_muscle == 'Legs':
                workout_image = account + '/static/img/quads.jpg'
            elif target_muscle == 'Traps':
                workout_image = account + '/static/img/traps.jpg'
            elif target_muscle == 'Back':
                workout_image = account + '/static/img/lats.jpg'
            elif target_muscle == 'Forearm':
                workout_image = account + '/static/img/forearm.jpg'
            elif target_muscle == 'Calves':
                workout_image = account + '/static/img/calf.jpg'
            elif target_muscle == 'Abs':
                workout_image = account + '/static/img/abs.jpg'

            #     Need to add default image

            return workout_image