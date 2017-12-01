import os
import sys

# Check the input arguments to decided action.
# DEFAULT: create
action = ''
if len(sys.argv) < 2:
    action = 'create'
else:
    action = sys.argv[1]

# If action was 'help' print out script syntax and exit
if action == 'help' or action == '--help':
    print('Usage: %s [create|school|delete] [school_name]' % sys.argv[0])
    sys.exit(0)

# Load the django instance
from django.core.wsgi import get_wsgi_application
from django.core.exceptions import ObjectDoesNotExist

# Point django to correct folders and files
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "."
sys.path.append(proj_path)
application = get_wsgi_application()

# Import models for editing
from django.contrib.auth.models import User, Group
from streamwebs.models import School, UserProfile

# Define account details

email = 'streamwebs@osuosl.org'
birthdate = '1980-01-01'
super_admin_name = 'superadmin'
org_admin_name = 'teacher'
org_author_name = 'student'

# Check to see if there are any schools in the database at all
if School.objects.all().exists():
    default_school = School.objects.order_by('name').first()
else:
    print('ERROR: There must be at least one school in the database, run the get_all.sh script')
    sys.exit(1)

# Create action
# Description: creates all the dev accounts and profiles
if action == 'create':

    # Pull the school name from the command line or use the default school
    if len(sys.argv) < 3:
        school = default_school
    else:
        school_name = ' '.join(sys.argv[2:])
        school = School.objects.filter(name=school_name).first()
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

# School action
# Description: will change the org_admin's and org_author's school link
elif action == 'school':

    # Pull the shcool name from the arguments, else use the default school
    if len(sys.argv) < 3:
        school = default_school
    else:
        school_name = ' '.join(sys.argv[2:])
        school = School.objects.filter(name=school_name).first()
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

# Delete action
# Description: will delete all the dev accounts
elif action == 'delete':

    # Delete the super admin
    super_admin_account = User.objects.filter(username=super_admin_name).first()
    if super_admin_account:
        super_admin_account.delete()
        print('\'' + super_admin_name + '\' user deleted')
    else:
        print('\'' + super_admin_name + '\' user didn\'t exist')

    # Delete the org admin
    org_admin_account = User.objects.filter(username=org_admin_name).first()
    if org_admin_account:
        org_admin_profile = UserProfile.objects.filter(user=org_admin_account).first()
        org_admin_account.delete()
        if org_admin_profile:
            org_admin_profile.delete()
        print('\'' + org_admin_name + '\' user deleted')
    else:
        print('\'' + org_admin_name + '\' user didn\'t exist')

    # Delete the org author
    org_author_account = User.objects.filter(username=org_author_name).first()
    if org_author_account:
        org_author_profile = UserProfile.objects.filter(user=org_author_account).first()
        org_author_account.delete()
        if org_author_profile:
            org_author_profile.delete()
        print('\'' + org_author_name + '\' user deleted')
    else:
        print('\'' + org_author_name + '\' user didn\'t exist')
