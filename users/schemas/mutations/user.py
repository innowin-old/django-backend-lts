from graphene import relay, Field, List, String, Boolean, ID
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.signing import TimestampSigner
from django.template import loader
from graphql_relay.node.node import from_global_id

from danesh_boom.viewer_fields import ViewerFields
from users.schemas.queries.user import UserNode, ProfileNode
from users.models import Education
from users.forms import ProfileForm, RegisterUserForm


class RegisterUserMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        username = String()
        email = String()
        password = String()

    user = Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # create user
        form = RegisterUserForm(input, initial={'is_active': False})
        if form.is_valid():
            user = form.save()
        else:
            raise Exception(str(form.errors))

        # set password
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        # create user Profile
        Profile.objects.create(user=user)

        # send activation email
        from_email = 'info@daneshboom.com'
        to_email = user.email
        signer = TimestampSigner()
        token = signer.sign(user.pk)
        subject = "Activation Email"
        current_site = get_current_site(context)
        domain = current_site.domain
        context = {
            'email': user.email,
            'domain': domain,
            'user': user,
            'token': token,
            'protocol': 'http',
        }
        email_template = html_email_template = "activation_email.html"
        body = loader.render_to_string(email_template, context)

        email_message = EmailMultiAlternatives(
            subject, body, from_email, [to_email])
        html_email = loader.render_to_string(html_email_template, context)
        email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

        return RegisterUserMutation(user=user)


class ChangePasswordMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        old_password = String()
        new_password = String()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        old_password = input.get('old_password')
        new_password = input.get('new_password')

        if user.has_usable_password():
            if not user.check_password(old_password):
                raise Exception("Invalid Password")

        # change password
        user.set_password(new_password)
        user.save()

        return ChangePasswordMutation(success=True)


class PasswordResetMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        email = String()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        email = input.get('email')

        form = PasswordResetForm(input)
        form.email = email
        if form.is_valid():
            opts = {
                'use_https': context.is_secure(),
                'from_email': 'info@daneshboom.com',
                'email_template_name': 'password_reset_email.html',
                'request': context,
                #'subject_template_name': subject_template_name,
                #'html_email_template_name': html_email_template_name,
            }
            form.save(**opts)

        return PasswordResetMutation(success=True)


class UpdateProfileMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        public_email = String()
        national_code = String()
        birth_date = String()
        web_site = List(String)
        phone = List(String)
        mobile = List(String)
        fax = String()
        telegram_account = String()
        description = String()

    profile = Field(ProfileNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):

        if hasattr(context.user, 'profile'):
            profile = context.user.profile
        else:
            profile = Profile()
            profile.user = context.user

        # update profile
        form = ProfileForm(input, instance=profile)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateProfileMutation(profile=profile)
