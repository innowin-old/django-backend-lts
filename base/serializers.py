from rest_framework.serializers import ModelSerializer
from django.db.models import Q

from users.models import Identity, Profile, StrengthStates
from .models import (
    Base,
    HashtagParent,
    Hashtag,
    BaseComment,
    Post,
    BaseCertificate,
    BaseRoll,
    RollPermission,
    HashtagRelation,
    BaseCountry,
    BaseProvince,
    BaseTown
)


class BaseSerializer(ModelSerializer):
    class Meta:
        model = Base
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class HashtagParentSerializer(BaseSerializer):
    class Meta:
        model = HashtagParent
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class HashtagSerializer(BaseSerializer):
    class Meta:
        model = Hashtag
        exclude = ['child_name']
        extra_kwargs = {
            'related_parent': {'read_only': True},
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        instance = Hashtag.objects.create(**validated_data)
        if HashtagParent.objects.filter(title=validated_data['title']).count() == 0:
            parent_instance = HashtagParent.objects.create(title=validated_data['title'])
        else:
            parent_instance = HashtagParent.objects.get(title=validated_data['title'])
            parent_instance.usage += 1
            parent_instance.save()
        instance.related_parent = parent_instance
        instance.save()
        self.check_hashtag_profile_strength()
        return instance

    def check_hashtag_profile_strength(self):
        request = self.context.get("request")
        try:
            identity = Identity.objects.get(identity_user=request.user)
        except Identity.DoesNotExist:
            identity = Identity.objects.create(identity_user=request.user)
        hashtags = Hashtag.objects.filter(hashtag_base=identity)
        try:
            user_strength = StrengthStates.objects.get(strength_user=request.user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(strength_user=request.user)
        if user_strength.hashtags_obtained is False and hashtags.count() == 3:
            try:
                profile = Profile.objects.get(profile_user=request.user)
            except Profile.DoesNotExist:
                return False
            profile.profile_strength += 10
            profile.save()
            user_strength.hashtags_obtained = True
            user_strength.save()


class HashtagRelationSerializer(BaseSerializer):
    class Meta:
        model = HashtagRelation
        depth = 1
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class BaseCommentSerializer(BaseSerializer):
    class Meta:
        model = BaseComment
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'comment_sender': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if 'comment_sender' not in validated_data or not request.user.is_superuser:
            identity = Identity.objects.get(identity_user=request.user)
            validated_data['comment_sender'] = identity
        comment = BaseComment.objects.create(**validated_data)
        return comment


class PostSerializer(BaseSerializer):
    class Meta:
        model = Post
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'post_user': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(**validated_data, post_user=request.user)
        post.save()
        if post.post_type == 'post':
            self.check_post_profile_strength()
        else:
            self.check_demand_supply_profile_strength()
        return post

    def check_post_profile_strength(self):
        request = self.context.get('request')
        posts = Post.objects.filter(post_user=request.user, post_type='post')
        try:
            user_strength = StrengthStates.objects.get(strength_user=request.user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(strength_user=request.user)
        if user_strength.post_obtained is False and posts.count() == 1:
            try:
                profile = Profile.objects.get(profile_user=request.user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(profile_user=request.user)
            profile.profile_strength += 5
            profile.save()
            user_strength.post_obtained = True
            user_strength.save()

    def check_demand_supply_profile_strength(self):
        request = self.context.get('request')
        posts = Post.objects.filter(Q(post_user=request.user), Q(post_type='supply') | Q(post_type='demand'))
        try:
            user_strength = StrengthStates.objects.get(strength_user=request.user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(strength_user=request.user)
        if user_strength.supply_demand_obtained is False and posts.count() == 1:
            try:
                profile = Profile.objects.get(profile_user=request.user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(profile_user=request.user)
            profile.profile_strength += 10
            profile.save()
            user_strength.supply_demand_obtained = True
            user_strength.save()


class PostListSerializer(BaseSerializer):
    class Meta:
        model = Post
        exclude = ['child_name']
        depth = 1
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'post_user': {'read_only': True}
        }


class CertificateSerializer(BaseSerializer):
    class Meta:
        model = BaseCertificate
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class RollSerializer(BaseSerializer):
    class Meta:
        model = BaseRoll
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class RollPermissionSerializer(BaseSerializer):
    class Meta:
        model = RollPermission
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class BaseCountrySerializer(BaseSerializer):
    class Meta:
        model = BaseCountry
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class BaseProvinceSerializer(BaseSerializer):
    class Meta:
        model = BaseProvince
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class BaseTownSerializer(BaseSerializer):
    class Meta:
        model = BaseTown
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }