from django.core.management.base import BaseCommand
from users.models import Role, User

class Command(BaseCommand):
    help = 'Manage users and roles'

    def add_arguments(self, parser):
        parser.add_argument('--create-role', type=str, help='Create a new role')
        parser.add_argument('--create-user', nargs=3, metavar=('NAME', 'EMAIL', 'ROLE'), help='Create a new user: name email role')
        parser.add_argument('--change-role', nargs=2, metavar=('EMAIL', 'NEW_ROLE'), help='Change user role: email new_role')
        parser.add_argument('--list-users', action='store_true', help='List all users')

    def handle(self, *args, **options):
        if options['create_role']:
            role_name = options['create_role']
            if role_name in ['admin', 'user']:
                role, created = Role.objects.get_or_create(name=role_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Role "{role_name}" created'))
                else:
                    self.stdout.write(f'Role "{role_name}" already exists')
            else:
                self.stdout.write(self.style.ERROR('Invalid role. Choose admin or user'))

        elif options['create_user']:
            name, email, role_name = options['create_user']
            try:
                role = Role.objects.get(name=role_name)
                user = User.objects.create(name=name, email=email, role=role)
                self.stdout.write(self.style.SUCCESS(f'User "{name}" created with role "{role_name}"'))
            except Role.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Role "{role_name}" does not exist'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(str(e)))

        elif options['change_role']:
            email, new_role_name = options['change_role']
            try:
                user = User.objects.get(email=email)
                new_role = Role.objects.get(name=new_role_name)
                user.role = new_role
                user.save()
                self.stdout.write(self.style.SUCCESS(f'User "{user.name}" role changed to "{new_role_name}"'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User with email "{email}" does not exist'))
            except Role.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Role "{new_role_name}" does not exist'))

        elif options['list_users']:
            users = User.objects.all()
            for user in users:
                self.stdout.write(f'{user.name} - {user.email} - {user.role.name}')

        else:
            self.stdout.write('Use --help for options')