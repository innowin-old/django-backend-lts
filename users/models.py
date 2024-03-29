from __future__ import unicode_literals

import re
import uuid
import random

from django.db import models, transaction
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from danesh_boom.models import PhoneField
from django.contrib.postgres.fields import JSONField
from media.models import Media
from organizations.models import Organization
from base.models import Base, BaseManager, BaseCountry, BaseProvince, BaseTown
from base.signals import update_cache, set_child_name


class Identity(Base):
    identity_user = models.OneToOneField(
        User,
        related_name="identity",
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        blank=True,
        help_text='Integer')
    identity_organization = models.OneToOneField(
        Organization,
        related_name="identity",
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        blank=True,
        help_text='Integer')
    name = models.CharField(max_length=150, db_index=True, unique=True, help_text='String(150)')
    accepted = models.BooleanField(default=False, db_index=True)
    mobile_verified = models.BooleanField(default=False, db_index=True)
    email_verified = models.BooleanField(default=False, db_index=True)

    objects = BaseManager()

    def clean(self):
        if not self.identity_user and not self.identity_organization:
            raise ValidationError(_('User or Organization should be set'))
        if self.identity_user and self.identity_organization:
            raise ValidationError(
                _('Only on of User or Organization should be set'))

    def __str__(self):
        return self.name

    def validate_user(self, identity_user):
        if self.identity_user and self.identity_user == identity_user:
            return True
        elif self.identity_organization and self.identity_organization.owner == identity_user:
            return True
        return False

    def validate_organization(self, identity_organization):
        if self.identity_organization == identity_organization:
            return True
        return False

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Identity, self).save(*args, **kwargs)


default_user_save = User.save
# Cache Model Data After Update
post_save.connect(update_cache, sender=Identity)
# Set Child Name
pre_save.connect(set_child_name, sender=Identity)


def user_save(self, *args, **kwargs):
    with transaction.atomic():
        default_user_save(self, *args, **kwargs)
        if hasattr(self, 'identity'):
            identity = self.identity
        else:
            identity = Identity(identity_user=self)
        identity.name = self.username
        identity.save()


User.save = user_save


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(profile_user=instance)
        profile.profile_secret_key = str(uuid.uuid4())
        headers = DefaultHeader.objects.all()
        if headers.count() > 0:
            profile.profile_banner_id = headers[random.randint(0, headers.count())].id
        profile.save()


class Profile(Base):
    GENDER = (
        ('male', 'مرد'),
        ('female', 'زن')
    )
    profile_user = models.OneToOneField(User, related_name="profile", db_index=True,
                                        on_delete=models.CASCADE, help_text='Integer')
    public_email = models.EmailField(null=True, blank=True, help_text='Email', db_index=True)
    national_code = models.CharField(max_length=10, blank=True, db_index=True,
                                     validators=[RegexValidator('^\d{10}$')], help_text='String(20)')
    profile_media = models.ForeignKey(Media, on_delete=models.CASCADE, db_index=True, related_name="users_profile_media",
                                      help_text='Integer', blank=True, null=True)
    birth_date = models.CharField(max_length=10, blank=True, db_index=True, null=True, help_text='String(10)')
    web_site = models.CharField(max_length=256, blank=True, db_index=True, null=True, help_text='Text')
    phone = models.CharField(max_length=11, blank=True, null=True, help_text='Phone', validators=[RegexValidator('^[0][0-9]{10,10}$')], db_index=True)
    mobile = models.CharField(max_length=11, blank=True, null=True, help_text='Phone', validators=[RegexValidator('^[0][9][0-9]{9,9}$')], db_index=True)
    auth_mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, db_index=True,
                                   validators=[RegexValidator('^[0][9][0-9]{9,9}$')], help_text='Phone')
    fax = PhoneField(blank=True, help_text='Phone', db_index=True)
    telegram_account = models.CharField(
        max_length=256, blank=True, db_index=True, help_text='String(256)')
    instagram_account = models.CharField(max_length=256, db_index=True, blank=True, help_text='String(256)')
    linkedin_account = models.CharField(max_length=256, db_index=True, blank=True, help_text='String(256)')
    description = models.TextField(blank=True, db_index=True, help_text='Text', max_length=70)
    gender = models.CharField(
        choices=GENDER,
        max_length=7,
        default='Male',
        help_text='Male | Female',
        db_index=True,
    )
    is_plus_user = models.BooleanField(default=False, db_index=True)
    is_user_organization = models.BooleanField(default=False, db_index=True)
    google_plus_address = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    social_image_url = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    linkedin_headline = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    linkedin_positions = models.TextField(blank=True, null=True, db_index=True)
    yahoo_contacts = models.TextField(blank=True, null=True, db_index=True)
    profile_strength = models.SmallIntegerField(default=10, db_index=True)
    address = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    profile_related_country = models.ForeignKey(BaseCountry, related_name='profile_country', db_index=True, blank=True
                                                , null=True, on_delete=models.CASCADE, help_text='Integer')
    profile_related_province = models.ForeignKey(BaseProvince, related_name='profile_province', db_index=True,
                                                 blank=True,
                                                 null=True, on_delete=models.CASCADE, help_text='Integer')
    profile_related_town = models.ForeignKey(BaseTown, related_name='profile_town', db_index=True, blank=True,
                                             null=True,
                                             on_delete=models.CASCADE, help_text='Integer')
    profile_banner = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="users_banner_media",
                                       help_text='Integer', blank=True, null=True, db_index=True)
    profile_secret_key = models.CharField(blank=True, null=True, max_length=100, db_index=True)

    objects = BaseManager()

    def __str__(self):
        return self.profile_user.username

    def clean(self):
        if self.birth_date:
            p = re.compile('^\d{4}-\d{2}-\d{2}$')
            birth_date = self.birth_date
            if not re.match(p, birth_date):
                raise ValidationError(_('Invalid birth date'))
            now = timezone.now().date().strftime('%Y-%m-%d')
            if birth_date > now:
                raise ValidationError(_('Invalid birth date'))


# Cache Model Data After Update
post_save.connect(update_cache, sender=Profile)
# Set Child Name
pre_save.connect(set_child_name, sender=Profile)


@receiver(post_save, sender=User)
def create_setting(sender, instance, created, **kwargs):
    if created:
        Setting.objects.create(setting_user=instance)


class Setting(Base):
    USER_TYPE = (
        ('all', "همه ی کاربران"),
        ('followers', "دنبال کنندگان"),
        ('no body', "هیچ کس"),
    )
    ACCOUNT_TYPE = (
        ('public', "عمومی"),
        ('private', "خصوصی"),
    )
    setting_user = models.OneToOneField(User, related_name="setting", db_index=True,
                                        on_delete=models.CASCADE, help_text='Integer')
    image_auto_download = models.BooleanField(default=True, help_text='Boolean', db_index=True)
    video_auto_download = models.BooleanField(default=True, help_text='Boolean', db_index=True)
    who_can_read_base_info = models.CharField(choices=USER_TYPE, db_index=True, default='all', max_length=10, help_text='all | followers | no body')
    who_can_read_activity = models.CharField(choices=USER_TYPE, db_index=True, default='all', max_length=10, help_text='all | followers | no body')
    who_can_read_work_experiences = models.CharField(choices=USER_TYPE, db_index=True, default='all', max_length=10, help_text='all | followers | no body')
    who_can_read_badges = models.CharField(choices=USER_TYPE, db_index=True, default='all', max_length=10, help_text='all | followers | no body')
    who_can_read_certificates = models.CharField(choices=USER_TYPE, db_index=True, default='all', max_length=10, help_text='all | followers | no body')
    who_can_read_followers = models.CharField(choices=USER_TYPE, db_index=True, default='all', max_length=10, help_text='all | followers | no body')
    who_can_read_followings = models.CharField(choices=USER_TYPE, db_index=True, default='all', max_length=10, help_text='all | followers | no body')
    who_can_read_exchanges = models.CharField(choices=USER_TYPE, db_index=True, default='all', max_length=10, help_text='all | followers | no body')
    can_search_engins_index_me = models.BooleanField(default=False, db_index=True)
    account_type = models.CharField(choices=ACCOUNT_TYPE, db_index=True, default='public', max_length=10, help_text='public | private')
    send_notifications_by_email = models.BooleanField(default=True, db_index=True, help_text='Boolean')
    send_follow_requests_by_email = models.BooleanField(default=False, db_index=True, help_text='Boolean')
    send_join_exchange_join_by_email = models.BooleanField(default=False, db_index=True, help_text='Boolean')
    send_supply_demand_recommends_by_email = models.BooleanField(default=False, db_index=True, help_text='Boolean')
    send_messages_notifications_by_email = models.BooleanField(default=False, db_index=True, help_text='Boolean')
    send_exchange_updates_by_email = models.BooleanField(default=False, db_index=True, help_text='Boolean')


class Education(Base):
    EDUCATION_GRADE = (
        ('Bachelor', "کارشناسی"),
        ('Master', "کارشناسی ارشد"),
        ('Phd', "دکتری"),
    )
    education_user = models.ForeignKey(User, related_name="educations", db_index=True,
                                       on_delete=models.CASCADE, help_text='Integer')
    grade = models.CharField(choices=EDUCATION_GRADE, db_index=True, default='Bachelor', max_length=10, help_text='Bachelor | Master | Phd')
    university = models.CharField(max_length=100, db_index=True, help_text='String(100)')
    field_of_study = models.CharField(max_length=100, db_index=True, help_text='String(100)')
    from_date = models.CharField(max_length=10, db_index=True, blank=True, null=True, help_text='String(7)')
    to_date = models.CharField(max_length=10, db_index=True, blank=True, null=True, help_text='String(7)')
    average = models.FloatField(
        validators=[
            MaxValueValidator(20),
            MinValueValidator(0)],
        null=True,
        blank=True,
        help_text='Float')
    description = models.TextField(blank=True, db_index=True, help_text='Text', max_length=30)

    objects = BaseManager()

    def __str__(self):
        return "%s(%s - %s)" % (
            self.education_user.username,
            self.grade,
            self.field_of_study
        )

    def clean(self):
        p = re.compile('^\d{4}-\d{2}$')
        from_date = to_date = None
        if self.from_date:
            from_date = self.from_date
            if not re.match(p, from_date):
                raise ValidationError(_('Invalid from date'))

        if self.to_date:
            to_date = self.to_date
            if not re.match(p, to_date):
                raise ValidationError(_('Invalid to date'))

        if from_date and to_date and from_date > to_date:
            raise ValidationError(_('To date must be greater than from date'))


# Cache Model Data After Update
post_save.connect(update_cache, sender=Education)
# Set Child Name
pre_save.connect(set_child_name, sender=Education)


class Research(Base):
    research_user = models.ForeignKey(User, related_name="researches", db_index=True,
                                      on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=250, help_text='String(250)', db_index=True)
    url = models.URLField(blank=True, help_text='URL', db_index=True)
    author = ArrayField(models.CharField(max_length=100), db_index=True, blank=True, help_text='Array(String(100))')
    publication = models.CharField(max_length=100, db_index=True, blank=True, help_text='String(100)')
    year = models.IntegerField(null=True, blank=True, db_index=True, help_text='Integer')
    page_count = models.IntegerField(null=True, db_index=True, blank=True, help_text='Integer')
    research_link = models.CharField(max_length=255, db_index=True, blank=True, null=True, help_text='String(255)')

    objects = BaseManager()

    def __str__(self):
        return "%s(%s)" % (self.research_user.username, self.title)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Research)
# Set Child Name
pre_save.connect(set_child_name, sender=Research)


class Certificate(Base):
    certificate_user = models.ForeignKey(User, related_name="certificates", db_index=True,
                                         on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=250, help_text='String(250)', db_index=True)
    picture_media = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=True,
        help_text='Integer')

    objects = BaseManager()

    def __str__(self):
        return "%s(%s)" % (self.certificate_user.username, self.title)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Certificate)
# Set Child Name
pre_save.connect(set_child_name, sender=Certificate)


class WorkExperience(Base):
    STATUSES = (
        ('WITHOUT_CONFIRM', 'بدون تایید'),
        ('WAIT_FOR_CONFIRM', 'منتظر تایید'),
        ('CONFIRMED', 'تایید شده'),
        ('UNCONFIRMED', 'تایید نشده'),
    )

    work_experience_user = models.ForeignKey(User, related_name="work_experiences", db_index=True,
                                             on_delete=models.CASCADE, help_text='Integer')
    name = models.CharField(max_length=100, blank=True, help_text='String(100)', db_index=True)
    work_experience_organization = models.ForeignKey(
        Organization,
        related_name="work_experience_organization",
        on_delete=models.CASCADE,
        help_text='Integer',
        db_index=True)
    position = models.CharField(max_length=100, blank=True, help_text='String(100)', db_index=True)
    from_date = models.CharField(max_length=10, blank=True, null=True, help_text='String(10)', db_index=True)
    to_date = models.CharField(max_length=10, blank=True, null=True, help_text='String(10)', db_index=True)
    status = models.CharField(
        choices=STATUSES,
        max_length=20,
        default='WITHOUT_CONFIRM',
        db_index=True,
        help_text='WITHOUT_CONFIRM | WAIT_FOR_CONFIRM | CONFIRMED | UNCONFIRMED')

    objects = BaseManager()

    def __str__(self):
        return "%s(%s)" % (self.work_experience_user.username, self.name)

    def clean(self):
        if not self.work_experience_organization and not self.name:
            raise ValidationError(_('Please enter name or organization'))

        if self.work_experience_organization and self.name:
            raise ValidationError(_('Please enter name or organization'))

        if self.name and self.status != 'WITHOUT_CONFIRM':
            raise ValidationError(_('Invalid status'))

        p = re.compile('^\d{4}-\d{2}$')
        from_date = to_date = None
        if self.from_date:
            from_date = self.from_date
            if not re.match(p, from_date):
                raise ValidationError(_('Invalid from date'))

        if self.to_date:
            to_date = self.to_date
            if not re.match(p, to_date):
                raise ValidationError(_('Invalid to date'))

        if from_date and to_date and from_date > to_date:
            raise ValidationError(_('To date must be greater than from date'))


# Cache Model Data After Update
post_save.connect(update_cache, sender=WorkExperience)
# Set Child Name
pre_save.connect(set_child_name, sender=WorkExperience)


class Skill(Base):
    skill_user = models.ForeignKey(User, related_name="skills", db_index=True,
                                   on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=250, help_text='String(250)', db_index=True)
    tag = ArrayField(models.CharField(max_length=50), blank=True, help_text='50', db_index=True)
    description = models.TextField(blank=True, help_text='Text', db_index=True)

    objects = BaseManager()

    def __str__(self):
        return "%s(%s)" % (self.skill_user.username, self.title)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Skill)
# Set Child Name
pre_save.connect(set_child_name, sender=Skill)


class IdentityUrl(Base):
    url = models.CharField(max_length=50, db_index=True, help_text='String(50)', unique=True)
    identity_url_related_identity = models.OneToOneField(Identity, related_name='urls', on_delete=models.CASCADE,
                                                         help_text='Integer', db_index=True)


# Cache Model Data After Update
post_save.connect(update_cache, sender=IdentityUrl)
# Set Child Name
pre_save.connect(set_child_name, sender=IdentityUrl)


class UserArticle(Base):
    user_article_related_user = models.ForeignKey(User, related_name="articles", db_index=True,
                                                  on_delete=models.CASCADE, help_text='Integer')
    doi_link = models.URLField(db_index=True)
    doi_meta = JSONField()
    publisher = models.CharField(max_length=100, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    article_author = ArrayField(models.CharField(max_length=255), blank=True, default=[], help_text='Array', db_index=True)


# Cache Model Data After Update
post_save.connect(update_cache, sender=UserArticle)
# Set Child Name
pre_save.connect(set_child_name, sender=UserArticle)


class AgentRequest(Base):
    # TODO
    """REQUEST_TYPES = (
        ('DIRECT_UPGRADE', 'ارتقا مستقیم به کارگزار'),
        ('RESUME_BASE_UPGRADE', ' ارتقا بر اساس سوابق کارگزاری '),
    )"""
    agent_request_identity = models.OneToOneField(Identity, related_name='agent', on_delete=models.CASCADE, help_text='Integer')
    agent_request_description = models.TextField()
    """agent_request_type = models.CharField(
        choices=REQUEST_TYPES,
        max_length=20,
        default='DIRECT_UPGRADE',
        help_text='DIRECT_UPGRADE | RESUME_BASE_UPGRADE')"""
    agent_request_accepted = models.BooleanField(default=False)


# Cache Model Data After Update
post_save.connect(update_cache, sender=AgentRequest)
# Set Child Name
pre_save.connect(set_child_name, sender=AgentRequest)


class Device(Base):
    device_user = models.ForeignKey(User, db_index=True, related_name='devices', on_delete=models.CASCADE, help_text='Integer')
    fingerprint = models.CharField(max_length=50, unique=True)
    browser_name = models.CharField(max_length=20, blank=True, null=True)
    browser_version = models.CharField(max_length=30, blank=True, null=True)
    browser_engine = models.CharField(max_length=20, blank=True, null=True)
    browser_engine_version = models.CharField(max_length=30, blank=True, null=True)
    device_os = models.CharField(max_length=20, blank=True, null=True)
    device_os_version = models.CharField(max_length=30, blank=True, null=True)
    device_type = models.CharField(max_length=10, blank=True, null=True)
    device_vendor = models.CharField(max_length=20, blank=True, null=True)
    device_cpu = models.CharField(max_length=10, blank=True, null=True)
    device_current_screen_resolution = models.CharField(max_length=12, blank=True, null=True)
    device_agent = models.CharField(max_length=255, blank=True, null=True)
    device_color_depth = models.SmallIntegerField(blank=True, null=True)
    ad_block = models.BooleanField(default=False)
    device_memory = models.IntegerField(blank=True, null=True)
    has_lied_browser = models.BooleanField(default=False)
    has_lied_languages = models.BooleanField(default=False)
    has_lied_os = models.BooleanField(default=False)
    has_lied_resolution = models.BooleanField(default=False)
    language = models.CharField(max_length=255, blank=True, null=True)
    timezone_offset = models.CharField(max_length=255, blank=True, null=True)
    touch_support = models.CharField(max_length=255, blank=True, null=True)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Device)
# Set Child Name
pre_save.connect(set_child_name, sender=Device)


@receiver(post_save, sender=User)
def create_strength(sender, instance, created, **kwargs):
    if created:
        StrengthStates.objects.create(strength_user=instance)


class StrengthStates(Base):
    strength_user = models.OneToOneField(User, related_name='strength', db_index=True, on_delete=models.CASCADE,
                                         help_text='Integer')
    registration_obtained = models.BooleanField(default=False)
    profile_media_obtained = models.BooleanField(default=False)
    first_last_name_obtained = models.BooleanField(default=False)
    hashtags_obtained = models.BooleanField(default=False)
    exchange_obtained = models.BooleanField(default=False)
    follow_obtained = models.BooleanField(default=False)
    post_obtained = models.BooleanField(default=False)
    supply_demand_obtained = models.BooleanField(default=False)
    certificate_obtained = models.BooleanField(default=False)
    badge_obtained = models.BooleanField(default=False)
    mobile_verification_obtained = models.BooleanField(default=False)
    email_verification_obtained = models.BooleanField(default=False)
    education_obtained = models.BooleanField(default=False)
    brought_obtained = models.BooleanField(default=False)
    work_obtained = models.BooleanField(default=False)


# Cache Model Data After Update
post_save.connect(update_cache, sender=StrengthStates)
# Set Child Name
pre_save.connect(set_child_name, sender=StrengthStates)


class UserMetaData(Base):
    META_TYPES = (
        ('phone', 'شماره تلفن'),
        ('mobile', 'شماه همراه'),
        ('email', 'آدرس ایمیل'),
    )
    user_meta_type = models.CharField(choices=META_TYPES, max_length=20, db_index=True)
    user_meta_value = models.CharField(max_length=20, db_index=True)
    user_meta_related_user = models.ForeignKey(User, related_name='meta_data_user', blank=True, null=True,
                                               db_index=True, on_delete=models.CASCADE, help_text='Integer')


# Cache Model Data After Update
post_save.connect(update_cache, sender=UserMetaData)
# Set Child Name
pre_save.connect(set_child_name, sender=UserMetaData)


class BlockIdentity(Base):
    blocked_identity = models.ForeignKey(Identity, related_name='blocked_identity', db_index=True,
                                         on_delete=models.CASCADE, help_text='Integer')
    blocker_identity = models.ForeignKey(Identity, related_name='blocker_identity', db_index=True,
                                         on_delete=models.CASCADE, help_text='integer')
    active_flag = models.BooleanField(default=True, db_index=True)


class UserCode(Base):
    TYPE_CHOICES = (
        ('email', 'Email'),
        ('sms', 'SMS'),
    )
    code = models.CharField(max_length=15, db_index=True, unique=True)
    user = models.ForeignKey(User, related_name='user_code', db_index=True, on_delete=models.CASCADE, help_text='Integer')
    active = models.BooleanField(default=True, db_index=True)
    used = models.BooleanField(default=False, db_index=True)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES, default='email', db_index=True)


class DefaultHeader(Base):
    default_header_related_file = models.ForeignKey(Media, related_name='default_header_related_file', db_index=True, on_delete=models.CASCADE, help_text='Integer')


class UniversityModel(Base):
    university_title = models.CharField(max_length=128, db_index=True, unique=True)
    university_town = models.ForeignKey(BaseTown, related_name="university_town", on_delete=models.CASCADE, db_index=True, help_text='Integer')


# post_save(update_cache, sender=University)


class UniversityField(Base):
    university_field_title = models.CharField(max_length=128, db_index=True, unique=True)


# post_save(update_cache, sender=UniversityField)