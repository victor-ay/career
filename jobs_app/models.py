from datetime import datetime

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    image = models.TextField(db_column="image", max_length=512, null=True, blank=True)
    is_talent = models.BooleanField(db_column="is_talent", null=True, blank=True)
    is_hiring = models.BooleanField(db_column="is_hiring", null=True, blank=True)

    class Meta:
        db_table = "user_profiles"

# class CV(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
#
#     class Meta:
#         db_table = "cvs"

class Company(models.Model):
    # TO DO :
    # Get more info about company
    # from link: https://www.linkedin.com/company/<company_id>/about/
    name = models.TextField(db_column="name", max_length=256, null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    industry = models.TextField(db_column="industry", max_length=512, default=None, null=True, blank=True)
    company_id_linkedin = models.TextField(db_column="company_id_linkedin", max_length=64, default=None, null=True, blank=True)
    company_linkedin_url = models.TextField(db_column="company_linkedin_url", max_length=256, default=None, null=True,
                                           blank=True)

    employees_min = models.IntegerField(db_column="employees_min", validators=[MinValueValidator(0), MaxValueValidator(1_000_000_000)], null=True, blank=True)
    employees_max = models.IntegerField(db_column="employees_max",
                                        validators=[MinValueValidator(0), MaxValueValidator(1_000_000_000)], null=True,
                                        blank=True)
    website = models.TextField(db_column="website", max_length=256, null=True, blank=True)
    logo_200_px = models.TextField(db_column="logo_200_px",
                                   max_length=512,
                                   default="https://cdn-icons-png.flaticon.com/256/3061/3061341.png",
                                   null=True, blank=True)
    logo_400_px = models.TextField(db_column="logo_400_px",
                                   max_length=512,
                                   default="https://cdn-icons-png.flaticon.com/512/3061/3061341.png",
                                   null=True, blank=True)
    list_my_jobs = models.BooleanField(db_column='list_my_jobs', default=True, blank=False, null=False)

    class Meta:
        db_table = "companies"


# class Branch(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.RESTRICT)
#     name = models.TextField(db_column="name",
#                             max_length=512,
#                             null=True, blank=True)
#     country = CountryField(blank= True, null= True)
#     state = models.TextField(db_column="state",
#                             max_length=256,
#                             null=True, blank=True)
#     city = models.TextField(db_column="city",
#                             max_length=256,
#                             null=True, blank=True)
#
#     # Defines the default Branch name as Company's name
#     def save(self, *args, **kwargs):
#         self.name.default = self.company_id.name
#         super().save(*args, **kwargs)  # Call the "real" save() method.
#
#
#     class Meta:
#         db_table = "branches"


class Job(models.Model):
    class JobSource(models.TextChoices):
        LINKEDIN = 'LinkedIn'
        GLASSDOOR = 'Glassdoor'
        FACEBOOK = 'Facebook'

    class EmploymentType(models.TextChoices):
        EMPLOYEE = 'Employee'
        PROJECT = 'Project'
        OUTSOURCE = 'Outsource'
        INTERN = 'Internship'

    class JobType(models.TextChoices):
        ON_SITE = 'On-site'
        REMOTE = 'Remote'
        HYBRID = 'Hybrid'

    class PaymentPeriodType(models.TextChoices):
        HOURLY = 'Hourly'
        MONTHLY = 'Monthly'
        ANNUALLY = 'Annually'
        PER_PROJECT = 'Per project'

    applicants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Application",
        related_name='jobs_applied'
    )

    favorited_by_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="FavoriteJobs",
        related_name='jobs_favorites'
    )
    # favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through="FavoriteJobs")

    company = models.ForeignKey(Company, default=None, on_delete=models.RESTRICT)
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null = True, blank=True, related_name='jobs_posted')



    # favorites = models

    source = models.TextField(db_column="source", choices=JobSource.choices ,null=False, blank=False)
    source_job_id = models.TextField(db_column="source_job_id", max_length=512, null=False, blank=False)
    is_active = models.BooleanField(db_column='is_active', null = True, blank=True)
    employment_type = models.TextField(db_column="employment_type",
                                       choices=EmploymentType.choices,
                                       default=EmploymentType.EMPLOYEE,
                                       null=False, blank=False)
    employment_percent = models.TextField(db_column="employment_percent",
                                             default='Full-time',
                                             null=False, blank=False)
    job_type = models.TextField(db_column="job_type",
                                       choices=JobType.choices,
                                       default=JobType.ON_SITE,
                                       null=False, blank=False)
    payment_period = models.TextField(db_column="payment_period",
                                       choices=PaymentPeriodType.choices,
                                       null=True, blank=True)
    payment_min = MoneyField(db_column='payment_min',
                             validators=[MinValueValidator(0)],
                             decimal_places=2,
                             max_digits=12, default_currency='USD',
                             null=True, blank=True)
    payment_max = MoneyField(db_column='payment_max',
                             validators=[MinValueValidator(0)],
                             decimal_places=2,
                             max_digits=12, default_currency='USD',
                             null=True, blank=True)
    # currency = MoneyField(db_column='currency', max_digits=12, default_currency='USD', null=True, blank=True)

    job_level = models.TextField(db_column="job_level", max_length=128, null=True, blank=True)
    title = models.TextField(db_column="title", max_length='1024', null=False, blank=False)
    description = models.TextField(db_column="description", max_length='65536', null=True, blank=True)
    location = models.TextField(db_column="location", max_length='1024', null=True, blank=True)
    application_url = models.TextField(db_column="application_url", max_length='2048', null=True, blank=True)
    posted_on_epoch = models.BigIntegerField(db_column='posted_on_epoch', null=True, blank=True)
    posted_on = models.DateTimeField(db_column='posted_on',default=datetime.now, blank=True)
    created_at = models.DateTimeField(db_column='created_at',auto_now_add=True)
    closed_at = models.DateTimeField(db_column='closed_at',null=True, blank=True)

    class Meta:
        db_table = "jobs"


class Application(models.Model):
    # class ApplicationStatus(models.TextChoices):
    #     APPLIED = 'Applied'
    #     APPROACHED = 'Approached'
    #     INTERVIEW = 'Interview'
    #     REJECTED = 'Rejected'
    #     CANCELED = 'Canceled'
    #     CONTRACT = 'Contract'
    #     HIRED = 'Hired'

    job = models.ForeignKey(Job, on_delete=models.RESTRICT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    # cv = models.ForeignKey(CV, on_delete=models.RESTRICT)
    application_date = models.DateTimeField(db_column='application_date',default=datetime.now, blank=True)
    is_deleted = models.BooleanField(db_column='is_deleted', default=False)


    class Meta:
        db_table = "applications"

class ApplicationFlow(models.Model):
    class ApplicationStatus(models.TextChoices):
        APPLIED = 'Applied'
        APPROACHED = 'Approached'
        INTERVIEW = 'Interview'
        REJECTED = 'Rejected'
        CANCELED = 'Canceled'
        CONTRACT = 'Contract'
        HIRED = 'Hired'

    application = models.ForeignKey(Application, on_delete=models.RESTRICT)
    status = models.TextField(db_column='status',
                              choices=ApplicationStatus.choices,
                              null=True, blank=True)
    created_at = models.DateTimeField(db_column='created_at', default=datetime.now, blank=True)
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)
    notes = models.TextField(db_column='notes', blank=True, null=True)
    to_do_date = models.DateTimeField(db_column='to_do_date', blank=True, null=True)
    to_do = models.TextField(db_column='to_do', max_length=1024, blank=True, null=True)
    is_deleted = models.BooleanField(db_column='is_deleted', default=False)


    class Meta:
        db_table = "application_flow"

class FavoriteJobs(models.Model):

    job = models.ForeignKey(Job, on_delete=models.RESTRICT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    action_date = models.DateTimeField(db_column='action_date', default=datetime.now, blank=True)
    # status = models.BooleanField(db_column='status', blank=True, null=True)

    class Meta:
        db_table = "favorite_jobs"

class Contact(models.Model):
    class ContactType(models.TextChoices):
        WEBSITE = 'Website'
        EMAIL = 'Email'
        PHONE = 'Phone'
        FACEBOOK = 'Facebook'
        LINKEDIN = 'LinkedIn'
        TWITTER = 'Twitter'
        GITHUB = 'Github'
        ADDRESS = 'Address'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    is_personal = models.BooleanField(default=True, blank=False, null=False)
    contact_type = models.TextField(db_column='contact_type',
                              choices=ContactType.choices,
                              null=True, blank=True)
    contact_point = models.TextField(db_column="contact_point", max_length=512, null=False, blank=False)

    class Meta:
        db_table = "contacts"


class HardSkill(models.Model):
    skill = models.TextField(db_column="skill", max_length=512, null=False, blank=False)

    class Meta:
        db_table = "hard_skills"


class HardSkillAbility(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.RESTRICT, blank=True, null=True)
    skill = models.ForeignKey(HardSkill, on_delete=models.RESTRICT)
    years_experience = models.IntegerField(db_column="years_experience",
                                           validators=[MinValueValidator(0), MaxValueValidator(80)],
                                           null=False, blank=False)

    class Meta:
        db_table = "hard_skills_abbility"


class SoftSkill(models.Model):
    skill = models.TextField(db_column="skill", max_length=512, null=False, blank=False)

    class Meta:
        db_table = "soft_skills"


class SoftSkillAbility(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.RESTRICT, blank=True, null=True)
    skill = models.ForeignKey(SoftSkill, on_delete=models.RESTRICT)


    class Meta:
        db_table = "soft_skills_abbility"


class Language(models.Model):
    skill = models.TextField(db_column="skill", max_length=512, null=False, blank=False)

    class Meta:
        db_table = "languages"


class LanguageAbility(models.Model):
    class LanguageLevel(models.TextChoices):
        NATIVE = 'Native'
        GREAT = 'Great'
        MEDIUM = 'Medium'
        OK = 'Ok'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.RESTRICT, blank=True, null=True)
    skill = models.ForeignKey(Language, on_delete=models.RESTRICT)

    read_write_level = models.TextField(db_column='read_write_level',
                                        choices=LanguageLevel.choices,
                                        default=LanguageLevel.GREAT,
                                        null=False, blank=False)
    verbal_level = models.TextField(db_column='verbal_level',
                                        choices=LanguageLevel.choices,
                                        default=LanguageLevel.GREAT,
                                        null=False)


    class Meta:
        db_table = "language_abbility"