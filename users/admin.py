from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from users.models import Profile, Education, Research, Certificate,\
    WorkExperience, Skill


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )


class EducationAdmin(admin.ModelAdmin):
    model = Education
    list_display = ['user', 'grade', 'university', 'field_of_study',
                    'from_date', 'to_date', 'average', 'description']


class ResearchAdmin(admin.ModelAdmin):
    model = Research
    list_display = ['user', 'title', 'author', 'publication', 'year']


class CertificateAdmin(admin.ModelAdmin):
    model = Certificate
    list_display = ['user', 'title']


class WorkExperienceAdmin(admin.ModelAdmin):
    model = WorkExperience
    list_display = ['user', 'name', 'position', 'from_date', 'to_date']


class SkillAdmin(admin.ModelAdmin):
    model = Skill
    list_display = ['user', 'title', 'tag']


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Skill, SkillAdmin)