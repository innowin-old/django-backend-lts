import django_filters
from django.contrib.auth.models import User
from django_filters import OrderingFilter
from graphene import relay, Field, AbstractType, resolve_only_args,\
    String, Int, List, ID
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

from danesh_boom.viewer_fields import ViewerFields
from organizations.models import Organization, StaffCount, Picture, Agent,\
    UserAgent
from users.schema import UserNode


#################### UserAgent #######################


class UserAgentFilter(django_filters.FilterSet):

    class Meta:
        model = UserAgent
        fields = {
            'id': ['exact'],
            # ---------- Organization ------------
            'organization_id': ['exact'],
            'organization__name': ['exact', 'icontains', 'istartswith'],
            # ---------- User ------------
            'user_id': ['exact'],
            'user__username': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(fields=('id',))


class UserAgentNode(DjangoObjectType):

    user = Field(UserNode)

    class Meta:
        model = UserAgent
        interfaces = (relay.Node, )


class CreateUserAgentMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        organization_id = String(required=True)
        user_id = String(required=True)
        agent_subject = String()

    user_agent = Field(UserAgentNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('organization_id')
        organization_id = from_global_id(organization_id)[1]
        organization = Organization.objects.get(pk=organization_id)

        user_agent_id = input.get('user_id')
        user_agent_id = from_global_id(user_agent_id)[1]
        user_agent = User.objects.get(pk=user_agent_id)

        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        agent_subject = input.get('agent_subject', '')

        # create user agent
        new_user_agent = UserAgent(
            organization=organization,
            user=user_agent,
            agent_subject=agent_subject,
        )
        try:
            new_user_agent.full_clean()
            new_user_agent.save()
        except Exception as e:
            raise Exception(str(e))

        return CreateUserAgentMutation(user_agent=new_user_agent)


class UpdateUserAgentMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        agent_subject = String()

    user_agent = Field(UserAgentNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        user_agent_id = from_global_id(id)[1]
        user_agent = UserAgent.objects.get(pk=user_agent_id)

        if user_agent.organization.user != user:
            raise Exception("Invalid Access to Organization")

        agent_subject = input.get('agent_subject', '')

        # update agent
        user_agent.agent_subject = agent_subject
        try:
            agent.full_clean()
            agent.save()
        except Exception as e:
            raise Exception(str(e))

        return UpdateUserAgentMutation(user_agent=user_agent)


class DeleteUserAgentMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        user_agent_id = from_global_id(id)[1]
        user_agent = UserAgent.objects.get(pk=user_agent_id)

        if user_agent.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete user agent
        user_agent.delete()

        return DeleteUserAgentMutation(deleted_id=id)


#################### Agent #######################

class AgentFilter(django_filters.FilterSet):

    class Meta:
        model = Agent
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'agent_subject': ['exact', 'icontains', 'istartswith'],
            'mobile': ['exact', 'icontains', 'istartswith'],
            'phone': ['exact', 'icontains', 'istartswith'],
            'email': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(
        fields=('id', 'agent_subject'))


class AgentNode(DjangoObjectType):

    class Meta:
        model = Agent
        interfaces = (relay.Node, )


class CreateAgentMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        organization_id = String(required=True)
        name = String(required=True)
        agent_subject = String()
        mobile = String(required=True)
        phone = String()
        email = String()

    agent = Field(AgentNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('organization_id')
        organization_id = from_global_id(organization_id)[1]
        organization = Organization.objects.get(pk=organization_id)

        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        name = input.get('name')
        agent_subject = input.get('agent_subject', '')
        mobile = input.get('mobile')
        phone = input.get('phone', '')
        email = input.get('email', '')

        # create agent
        new_agent = Agent(
            organization=organization,
            name=name,
            agent_subject=agent_subject,
            mobile=mobile,
            phone=phone,
            email=email
        )
        try:
            new_agent.full_clean()
            new_agent.save()
        except Exception as e:
            raise Exception(str(e))

        return CreateAgentMutation(agent=new_agent)


class UpdateAgentMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        name = String(required=True)
        agent_subject = String()
        mobile = String(required=True)
        phone = String()
        email = String()

    agent = Field(AgentNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        agent_id = from_global_id(id)[1]
        agent = Agent.objects.get(pk=agent_id)

        if agent.organization.user != user:
            raise Exception("Invalid Access to Organization")

        name = input.get('name')
        agent_subject = input.get('agent_subject', '')
        mobile = input.get('mobile')
        phone = input.get('phone', '')
        email = input.get('email', '')

        # update agent
        agent.name = name
        agent.agent_subject = agent_subject
        agent.mobile = mobile
        agent.phone = phone
        agent.email = email
        try:
            agent.full_clean()
            agent.save()
        except Exception as e:
            raise Exception(str(e))

        return UpdateAgentMutation(agent=agent)


class DeleteAgentMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        agent_id = from_global_id(id)[1]
        agent = Agent.objects.get(pk=agent_id)

        if agent.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete agent
        agent.delete()

        return DeleteAgentMutation(deleted_id=id)


#################### Picture #######################

class PictureFilter(django_filters.FilterSet):

    class Meta:
        model = Picture
        fields = {
            'id': ['exact'],
        }

    order_by = OrderingFilter(fields=('id', 'order'))


class PictureNode(DjangoObjectType):

    class Meta:
        model = Picture
        interfaces = (relay.Node, )


class CreatePictureMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        organization_id = String(required=True)
        order = Int(required=True)
        description = String()

    picture = Field(PictureNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('organization_id')
        organization_id = from_global_id(organization_id)[1]
        organization = Organization.objects.get(pk=organization_id)

        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        order = input.get('order')
        description = input.get('description', '')
        files = context.FILES
        picture = files.get('picture', None)
        if picture is None:
            raise Exception("Invalid Picture")

        # create picture
        new_picture = Picture(
            organization=organization,
            picture=picture,
            order=order,
            description=description,
        )
        try:
            new_picture.full_clean()
            new_picture.save()
        except Exception as e:
            raise Exception(str(e))

        return CreatePictureMutation(picture=new_picture)


class UpdatePictureMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        order = Int(requeired=True)
        description = String()

    picture = Field(PictureNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        picture_id = from_global_id(id)[1]
        picture = Picture.objects.get(pk=picture_id)

        if picture.organization.user != user:
            raise Exception("Invalid Access to Organization")

        order = input.get('order')
        description = input.get('description', '')

        # update picture
        picture.order = order
        picture.description = description
        try:
            picture.full_clean()
            picture.save()
        except Exception as e:
            raise Exception(str(e))

        return UpdatePictureMutation(picture=picture)


class DeletePictureMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        picture_id = from_global_id(id)[1]
        picture = Picture.objects.get(pk=picture_id)

        if picture.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete picture
        picture.delete()

        return DeletePictureMutation(deleted_id=id)


#################### StaffCount #######################

class StaffCountFilter(django_filters.FilterSet):

    class Meta:
        model = StaffCount
        fields = {
            'id': ['exact'],
            'count': ['exact', 'gte', 'lte'],
            'create_time': ['exact', 'gte', 'lte'],
        }

    order_by = OrderingFilter(fields=('id', 'count', 'create_time'))


class StaffCountNode(DjangoObjectType):

    class Meta:
        model = StaffCount
        interfaces = (relay.Node, )


class CreateStaffCountMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        organization_id = String(required=True)
        count = Int(requeired=True)

    staff_count = Field(StaffCountNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('organization_id')
        organization_id = from_global_id(organization_id)[1]
        organization = Organization.objects.get(pk=organization_id)

        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        count = input.get('count')

        # create staff count
        new_staff_count = StaffCount(
            organization=organization,
            count=count
        )
        try:
            new_staff_count.full_clean()
            new_staff_count.save()
        except Exception as e:
            raise Exception(str(e))

        return CreateStaffCountMutation(staff_count=new_staff_count)


class UpdateStaffCountMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        count = Int(requeired=True)

    staff_count = Field(StaffCountNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        staff_count_id = from_global_id(id)[1]
        staff_count = StaffCount.objects.get(pk=staff_count_id)

        if staff_count.organization.user != user:
            raise Exception("Invalid Access to Organization")

        count = input.get('count')

        # update staff count
        staff_count.count = count
        try:
            staff_count.full_clean()
            staff_count.save()
        except Exception as e:
            raise Exception(str(e))

        return UpdateStaffCountMutation(staff_count=staff_count)


class DeleteStaffCountMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        staff_count_id = from_global_id(id)[1]
        staff_count = StaffCount.objects.get(pk=staff_count_id)

        if staff_count.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete staff count
        staff_count.delete()

        return DeleteStaffCountMutation(deleted_id=id)


#################### Organization #######################

class OrganizationFilter(django_filters.FilterSet):

    class Meta:
        model = Organization
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'national_code': ['exact', 'icontains', 'istartswith'],
            'registrar_organization': ['exact', 'icontains', 'istartswith'],
            'country': ['exact', 'icontains', 'istartswith'],
            'province': ['exact', 'icontains', 'istartswith'],
            'city': ['exact', 'icontains', 'istartswith'],
            'ownership_type': ['exact', 'icontains', 'istartswith'],
            'business_type': ['exact', 'icontains', 'istartswith'],
            # ---------- User ------------
            'user_id': ['exact'],
            'user__username': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(fields=('id', 'established_year',))


class OrganizationNode(DjangoObjectType):

    organization_staff_counts = DjangoFilterConnectionField(
        StaffCountNode, filterset_class=StaffCountFilter)
    organization_pictures = DjangoFilterConnectionField(
        PictureNode, filterset_class=PictureFilter)
    organization_agents = DjangoFilterConnectionField(
        AgentNode, filterset_class=AgentFilter)
    organization_user_agents = DjangoFilterConnectionField(
        UserAgentNode, filterset_class=UserAgentFilter)

    @resolve_only_args
    def resolve_organization_staff_counts(self, **args):
        staff_counts = StaffCount.objects.filter(organization=self)
        return StaffCountFilter(args, queryset=staff_counts).qs

    @resolve_only_args
    def resolve_organization_pictures(self, **args):
        pictures = Picture.objects.filter(organization=self)
        return PictureFilter(args, queryset=pictures).qs

    @resolve_only_args
    def resolve_organization_agents(self, **args):
        agents = Agent.objects.filter(organization=self)
        return AgentFilter(args, queryset=agents).qs

    @resolve_only_args
    def resolve_organization_user_agents(self, **args):
        user_agents = UserAgent.objects.filter(organization=self)
        return UserAgentFilter(args, queryset=user_agents).qs

    class Meta:
        model = Organization
        interfaces = (relay.Node, )
        only_fields = [
            'id',
            'name',
            'national_code',
            'phone',
            'registration_ads_url',
            'registrar_organization',
            'country',
            'province',
            'city',
            'address',
            'web_site',
            'established_year',
            'ownership_type',
            'business_type',
            'logo',
            'description',
            'advantages',
            'correspondence_language']


class CreateOrganizationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        name = String(required=True)
        national_code = String(required=True)
        registration_ads_url = String()
        registrar_organization = String()
        country = String(required=True)
        province = String(required=True)
        city = String()
        address = String()
        phone = List(String)
        web_site = String()
        established_year = Int()
        ownership_type = String()
        business_type = String(required=True)
        description = String()
        advantages = String()
        correspondence_language = String()
        telegram_channel = String()

    organization = Field(OrganizationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        name = input.get('name')
        national_code = input.get('national_code')
        registration_ads_url = input.get('registration_ads_url', '')
        registrar_organization = input.get('registrar_organization', '')
        country = input.get('country')
        province = input.get('province')
        city = input.get('city', '')
        address = input.get('address', '')
        phone = input.get('phone', [])
        web_site = input.get('web_site', '')
        established_year = input.get('established_year', None)
        ownership_type = input.get('', 'oth')
        business_type = input.get('business_type', '')
        description = input.get('description', '')
        advantages = input.get('advantages', '')
        correspondence_language = input.get('correspondence_language', '')
        telegram_channel = input.get('telegram_channel', '')
        files = context.FILES
        logo = files.get('logo', None)

        # create organization
        new_organization = Organization(
            user=user,
            name=name,
            national_code=national_code,
            registration_ads_url=registration_ads_url,
            registrar_organization=registrar_organization,
            country=country,
            province=province,
            city=city,
            address=address,
            phone=phone,
            web_site=web_site,
            established_year=established_year,
            ownership_type=ownership_type,
            business_type=business_type,
            description=description,
            advantages=advantages,
            correspondence_language=correspondence_language,
            telegram_channel=telegram_channel,
            logo=logo,
        )
        try:
            new_organization.full_clean()
            new_organization.save()
        except Exception as e:
            raise Exception(str(e))

        return CreateOrganizationMutation(organization=new_organization)


class UpdateOrganizationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        name = String(required=True)
        national_code = String(required=True)
        registration_ads_url = String()
        registrar_organization = String()
        country = String(required=True)
        province = String(required=True)
        city = String()
        address = String()
        phone = List(String)
        web_site = String()
        established_year = Int()
        ownership_type = String()
        business_type = String(required=True)
        description = String()
        advantages = String()
        correspondence_language = String()
        telegram_channel = String()

    organization = Field(OrganizationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        organization_id = from_global_id(id)[1]
        organization = Organization.objects.get(pk=organization_id)
        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        name = input.get('name')
        national_code = input.get('national_code')
        registration_ads_url = input.get('registration_ads_url', '')
        registrar_organization = input.get('registrar_organization', '')
        country = input.get('country')
        province = input.get('province')
        city = input.get('city', '')
        address = input.get('address', '')
        phone = input.get('phone', [])
        web_site = input.get('web_site', '')
        established_year = input.get('established_year', None)
        ownership_type = input.get('', 'oth')
        business_type = input.get('business_type', '')
        description = input.get('description', '')
        advantages = input.get('advantages', '')
        correspondence_language = input.get('correspondence_language', '')
        telegram_channel = input.get('telegram_channel', '')
        files = context.FILES
        logo = files.get('logo', None)

        # update organization
        organization.name = name
        organization.national_code = national_code
        organization.registration_ads_url = registration_ads_url
        organization.registrar_organization = registrar_organization
        organization.country = country
        organization.province = province
        organization.city = city
        organization.address = address
        organization.phone = phone
        organization.web_site = web_site
        organization.established_year = established_year
        organization.ownership_type = ownership_type
        organization.business_type = business_type
        organization.description = description
        organization.advantages = advantages
        organization.correspondence_language = correspondence_language
        organization.telegram_channel = telegram_channel
        if logo:
            organization.logo = logo
        try:
            organization.full_clean()
            organization.save()
        except Exception as e:
            raise Exception(str(e))

        return UpdateOrganizationMutation(organization=organization)


class DeleteOrganizationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        organization_id = from_global_id(id)[1]
        organization = Organization.objects.get(pk=organization_id)
        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete organization
        organization.delete()

        return DeleteOrganizationMutation(deleted_id=id)


#################### Organization Query & Mutation #######################

class OrganizationQuery(AbstractType):

    organization = relay.Node.Field(OrganizationNode)
    organizations = DjangoFilterConnectionField(
        OrganizationNode, filterset_class=OrganizationFilter)


class OrganizationMutation(AbstractType):
    # ---------------- Organization ----------------
    create_organization = CreateOrganizationMutation.Field()
    update_organization = UpdateOrganizationMutation.Field()
    delete_organization = DeleteOrganizationMutation.Field()

    # ---------------- StaffCount ----------------
    create_organization_staff_count = CreateStaffCountMutation.Field()
    update_organization_staff_count = UpdateStaffCountMutation.Field()
    delete_organization_staff_count = DeleteStaffCountMutation.Field()

    # ---------------- Picture ----------------
    create_organization_picture = CreatePictureMutation.Field()
    update_organization_picture = UpdatePictureMutation.Field()
    delete_organization_picture = DeletePictureMutation.Field()

    # ---------------- Agent ----------------
    create_organization_agent = CreateAgentMutation.Field()
    update_organization_agent = UpdateAgentMutation.Field()
    delete_organization_agent = DeleteAgentMutation.Field()

    # ---------------- UserAgent ----------------
    create_organization_user_agent = CreateUserAgentMutation.Field()
    delete_organization_user_agent = DeleteUserAgentMutation.Field()
