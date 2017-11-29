import os
import sys

action = ''
if len(sys.argv) < 2:
    action = 'create'
else:
    action = sys.argv[1]

if action == 'help' or action == '--help':
    print('Usage: %s [create|school|delete] [school_name]' % sys.argv[0])
    sys.exit(0)

from django.core.wsgi import get_wsgi_application
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "."
sys.path.append(proj_path)
application = get_wsgi_application()

from django.contrib.auth.models import User, Group
from streamwebs.models import School, UserProfile

# Define account details

email = 'streamwebs@osuosl.org'
birthdate = '1980-01-01'
super_admin_name = 'superadmin'
org_admin_name = 'teacher'
org_author_name = 'student'

if School.objects.all().exists():
    default_school = School.objects.order_by('name').first()
else:
    print('ERROR: There must be at least one school in the database, run the get_all.sh script')
    sys.exit(1)

# Create action
if action == 'create':

    if len(sys.argv) < 3:
        school = default_school
    else:
        school = School.objects.filter(name=sys.argv[2]).first()
        if school is None:
            print('ERROR: couldn\'t find the school \'%s\'' % sys.argv[2])
            sys.exit(2)

    # Create Super Admin dev account

    super_admin, created = Group.objects.get_or_create(name='super_admin')

    if not User.objects.filter(username=super_admin_name).exists():
        sa_account, created = User.objects.get_or_create(
            username=super_admin_name,
            email=email
        )
        if created:
            sa_account.groups.add(super_admin)
            sa_account.set_password(super_admin_name)
            sa_account.save()
            print('\'' + super_admin_name + '\' user created')
    else:
        print('\'' + super_admin_name + '\' user exists')


    # Create Org Admin dev account

    org_admin, created = Group.objects.get_or_create(name='org_admin')

    if not User.objects.filter(username=org_admin_name).exists():
        oadmin_account, created = User.objects.get_or_create(
            username=org_admin_name,
            email=email
        )
        if created:
            oadmin_account.groups.add(org_admin)
            oadmin_account.set_password(org_admin_name)
            oadmin_account.save()
            try:
                oadmin_profile = UserProfile.objects.create(
                    user=oadmin_account,
                    school=school,
                    birthdate=birthdate
                )
                oadmin_account.save()
                print('\'' + org_admin_name + '\' user created, linked to school \'' + school.name + '\'')
            except:
                oadmin_account.delete()
                print('\'' + org_admin_name + '\' user not created, failed to create profile')
            
    else:
        user = User.objects.filter(username=org_admin_name).first()
        profile = UserProfile.objects.filter(user=user).first()
        if profile is None:
            print('\'' + org_admin_name + '\' user exists, with no profile')
        else:
            tmp_school = profile.school
            if tmp_school is None:
                print('\'' + org_admin_name + '\' user exists, no linked school')
            else:
                print('\'' + org_admin_name + '\' user exists, linked to school \'' + tmp_school.name + '\'')


    # Create Org Author dev account

    org_author, created = Group.objects.get_or_create(name='org_author')

    if not User.objects.filter(username=org_author_name).exists():
        author_account, created = User.objects.get_or_create(
            username=org_author_name,
            email=email
        )
        if created:
            author_account.groups.add(org_author)
            author_account.set_password(org_author_name)
            author_account.save()
            try:
                author_profile = UserProfile.objects.create(
                    user=author_account,
                    school=school,
                    birthdate=birthdate
                )
                author_profile.save()
                print('\'' + org_author_name + '\' user created, linked to school \'' + school.name + '\'')
            except:
                author_account.delete()
                print('\'' + org_author_name + '\' user not created, failed to create profile')
    else:
        user = User.objects.filter(username=org_author_name).first()
        profile = UserProfile.objects.filter(user=user).first()
        if profile is None:
            print('\'' + org_author_name + '\' user exists, with no profile')
        else:
            tmp_school = profile.school
            if tmp_school is None:
                print('\'' + org_author_name + '\' user exists, no linked school')
            else:
                print('\'' + org_author_name + '\' user exists, linked to school \'' + tmp_school.name + '\'')

elif action == 'school':
    if len(sys.argv) < 3:
        school = default_school
    else:
        school = School.objects.filter(name=sys.argv[2]).first()
        if school is None:
            print('ERROR: couldn\'t find the school \'%s\'' % sys.argv[2])
            sys.exit(2)

    # Change Org Admin School
    org_admin_account = User.objects.filter(username=org_admin_name).first()
    org_admin_profile = UserProfile.objects.filter(user=org_admin_account).first()
    org_admin_profile.school = school
    org_admin_profile.save()
    print('\'' + org_admin_name + '\' user linked to school \'' + school.name + '\'')

    # Change Org Author School
    org_author_account = User.objects.filter(username=org_author_name).first()
    org_author_profile = UserProfile.objects.filter(user=org_author_account).first()
    org_author_profile.school = school
    org_author_profile.save()
    print('\'' + org_author_name + '\' user linked to school \'' + school.name + '\'')

elif action == 'delete':
    super_admin_account = User.objects.filter(username=super_admin_name).first()
    super_admin_profile = UserProfile.objects.filter(user=super_admin_account).first()
    super_admin_account.delete()
    super_admin_profile.delete()
    print('\'' + super_admin_name + '\' user deleted')

    org_admin_account = User.objects.filter(username=org_admin_name).first()
    org_admin_profile = UserProfile.objects.filter(user=org_admin_account).first()
    org_admin_account.delete()
    org_admin_profile.delete()
    print('\'' + org_admin_name + '\' user deleted')

    org_author_account = User.objects.filter(username=org_author_name).first()
    org_author_profile = UserProfile.objects.filter(user=org_author_account).first()
    org_author_account.delete()
    org_author_profile.delete()
    print('\'' + org_author_name + '\' user deleted')
