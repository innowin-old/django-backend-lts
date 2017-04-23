from graphene import relay, Field, List, String, Int, ID

from danesh_boom.viewer_fields import ViewerFields
from organizations.models import Organization
from organizations.schemas.queries.organization import OrganizationNode
from organizations.forms import OrganizationForm
from media.models import Media
from utils.relay_helpers import get_node


class CreateOrganizationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        name = String(required=True)
        organ_name = String(required=True)
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
        business_type = List(String, required=True)
        logo_id = String()
        description = String()
        advantages = String()
        correspondence_language = List(String)
        telegram_channel = String()

    organization = Field(OrganizationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        logo_id = input.get('logo_id')
        logo = get_node(logo_id, context, info, Media)

        # create organization
        form = OrganizationForm(input)
        if form.is_valid():
            new_organization = form.save(commit=False)
            new_organization.user = user
            new_organization.logo = logo
            new_organization.save()
        else:
            raise Exception(str(form.errors))

        return CreateOrganizationMutation(organization=new_organization)


class UpdateOrganizationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        name = String(required=True)
        organ_name = String(required=True)
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
        business_type = List(String, required=True)
        logo_id = String()
        description = String()
        advantages = String()
        correspondence_language = List(String)
        telegram_channel = String()

    organization = Field(OrganizationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('id', None)
        organization = get_node(organization_id, context, info, Organization)

        if not organization:
            raise Exception("Invalid Organization")

        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        logo_id = input.get('logo_id')
        logo = get_node(logo_id, context, info, Media)

        # update organization
        organization.logo = logo
        form = OrganizationForm(input, instance=organization)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateOrganizationMutation(organization=organization)


class DeleteOrganizationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('id', None)
        organization = get_node(organization_id, context, info, Organization)

        if not organization:
            raise Exception("Invalid Organization")

        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete logo in media model
        organization.logo.delete()

        # delete organization
        organization.delete()

        return DeleteOrganizationMutation(deleted_id=id)
