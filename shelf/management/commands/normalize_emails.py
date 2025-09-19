from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

# class Command(BaseCommand):
#     help = "Normalize email addresses for all users"

#     def handle(self, *args, **kwargs):
#         User = get_user_model()
#         users = User.objects.all()
#         updated = 0
#         skipped = 0

#         with transaction.atomic():
#             for user in users:
#                 email = user.email
#                 if not email or '@' not in email:
#                     self.stdout.write(f"Skipping user — invalid email: {email}")
#                     skipped += 1
#                     continue

#                 normalized_email = email.lower().strip()
#                 if "@" not in normalized_email:
#                     self.stdout.write(f"this user doest have valid user{email}")
#                     normalized_email = normalized_email+"@unknown.com"

#                 if normalized_email != email:
#                     user.email = normalized_email
#                     user.save(update_fields=['email'])
#                     self.stdout.write(f"Updated: {email} → {normalized_email}")
#                     updated += 1
                

#         self.stdout.write(self.style.SUCCESS(f"Normalization complete. {updated} updated, {skipped} skipped."))
