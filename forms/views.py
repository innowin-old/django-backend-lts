from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .models import (
    Form,
    Group,
    Element,
    FormGroup,
    FormGroupElement,
    Data
)
from .serializers import (
    FormSerializer,
    GroupSerializer,
    ElementSerializer,
    FormGroupSerializer,
    FormGroupElementSerializer,
    DataSerializer
)

# Create your views here.
class FormViewSet(ModelViewSet):
    """
        A ViewSet for Handle Form Views
    """
    # queryset = Form.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Form.objects.all()

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)

        description = self.request.query_params.get('description', None)
        if description is not None:
            queryset = queryset.filter(description=description)

        return queryset

    def get_serializer_class(self):
        return FormSerializer


class GroupViewSet(ModelViewSet):
    """
        A ViewSet for Handle Group Views
    """
    # queryset = Group.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Group.objects.all()

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)

        return queryset

    def get_serializer_class(self):
        return GroupSerializer


class FormGroupViewSet(ModelViewSet):
    """
        A ViewSet for Handle Form Group Views
    """
    # queryset = FormGroup.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = FormGroup.objects.all()

        form_id = self.request.query_params.get('form_id', None)
        if form_id is not None:
            queryset = queryset.filter(form_form_id=form_id)

        form_title = self.request.query_params.get('form_title', None)
        if form_title is not None:
            queryset = queryset.filter(form_form__title__contains=form_title)

        form_group_id = self.request.query_params.get('group_id', None)
        if form_group_id is not None:
            queryset = queryset.filter(form_group_id=form_group_id)

        form_group_title = self.request.query_params.get('group_title', None)
        if form_group_title is not None:
            queryset = queryset.filter(form_group__title__contains=form_group_title)

        required = self.request.query_params.get('required', None)
        if required is not None:
            queryset = queryset.filter(required=required)

        return queryset

    def get_serializer_class(self):
        return FormGroupSerializer


class ElementViewSet(ModelViewSet):
    """
        A ViewSet for Handle Element Views
    """
    # queryset = Element.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Element.objects.all()

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset

    def get_serializer_class(self):
        return ElementSerializer


class FormGroupElementViewSet(ModelViewSet):
    """
        A ViewSet for Handle FormGroupElement Views
    """
    # queryset = FormGroupElement.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):

        queryset = FormGroupElement.objects.all()

        form_group_title = self.request.query_params.get('form_group_title', None)
        if form_group_title is not None:
            queryset = queryset.filter(form_form_group__form_form__title__contains=form_group_title)

        form_group_id = self.request.query_params.get('form_group_id', None)
        if form_group_id is not None:
            queryset = queryset.filter(form_form_group_id=form_group_id)

        form_element_name = self.request.query_params.get('form_element_name', None)
        if form_element_name is not None:
            queryset = queryset.filter(form_element__name=form_element_name)

        form_element_id = self.request.query_params.get('form_element_id', None)
        if form_element_id is not None:
            queryset = queryset.filter(form_element_id=form_element_id)

        return queryset

    def get_serializer_class(self):
        return FormGroupElementSerializer

class DataViewSet(ModelViewSet):
    """
        A ViewSet for Handle Data Views
    """
    # queryset = Data.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Data.objects.all()

        data = self.request.query_params.get('data', None)
        if data is not None:
            queryset = queryset.filter(data__contains=data)

        form_title = self.request.query_params.get('form_title', None)
        if form_title is not None:
            queryset = queryset.filter(form_group_element__form_form_group__form_form__title__contains=form_title)

        return queryset

    def get_serializer_class(self):
        return DataSerializer