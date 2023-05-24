import copy
import random

from django.db.models import Prefetch
from rest_framework import mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from jobs_app.models import Application, ApplicationFlow
from jobs_app.serializers.application_flow import ApplicationsFlowSerializerSimple
from jobs_app.serializers.applications import ApplicationsSerializer, ApplicationsStaffSerializer, \
    ApplicationPostSerializer


# class ApplicationsPermissions(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in ['GET'] and request.user.is_staff:
#             return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         pass

first_notes_congratulations = [
    "Congratulations on taking the exciting step of submitting your application for a new position! \nWishing you the best of luck in the selection process.",
    "Way to go! You've successfully submitted your application for a new position. \nSending you our heartfelt congratulations and positive vibes as you embark on this new professional journey.",
    "Congratulations on hitting the 'submit' button for your new position! Your determination and hard work have brought you one step closer to your career goals. \nKeep up the great work!",
    "Bravo! Your application for a new position has been submitted. This achievement reflects your dedication and readiness to pursue new opportunities. \nWishing you success as you await the next steps in the process."
    "Fantastic news! You've completed the first milestone by submitting your application for a new position. It's a testament to your skills and ambition. \nCongratulations and may this opportunity lead you to new heights in your career."
]

first_notes_suggestions = [
    "Suggestion from JobJolt - Leverage your network:\n"
    "Check if you have any connections at the company and reach out to them for insights or potential referrals. Personal recommendations can significantly improve your chances of being noticed.",
    "Suggestion from JobJolt - Request recommendations:\n"
    "If you have relevant recommendations on your LinkedIn profile, you can request specific recommendations from colleagues or supervisors that highlight your skills and achievements.",
    "Suggestion from JobJolt - Stay active and engaged:\n"
    "Engage with relevant industry groups, share insightful content, and participate in discussions. Active participation can enhance your visibility and demonstrate your expertise.",
    "Suggestion from JobJolt - Follow up:\n"
    "After submitting your application, consider sending a polite and concise follow-up message to express your interest in the position. This can demonstrate your enthusiasm and proactive attitude.",
    "Suggestion from JobJolt - Update your LinkedIn profile:\n"
    "Ensure that your profile is up to date with relevant work experience, skills, and a professional summary. Highlight your accomplishments and use keywords related to the job you're applying for.",
    "Suggestion from JobJolt - Research the company:\n"
    "Take the time to learn about the company you're applying to. Understand their values, culture, and mission. Incorporate this knowledge into your application to demonstrate your genuine interest."
]

first_notes_explanations = [
    "Why should you keep notes about the job submission process while looking for a new position?\n"
    "Keeping notes about the job submission process can be beneficial for several reasons:\n"
    "Organization: Taking notes helps you stay organized by keeping track of the positions you've applied to, the companies you've contacted, and the specific details of each application. It prevents confusion and ensures you have a clear overview of your job search progress.",
    "Application Follow-Up: When you keep notes about each job application, you can easily refer back to important details such as application deadlines, interview dates, and contact information. This makes it easier to follow up with employers, express continued interest, and ask relevant questions during the hiring process.",
    "Learning and Improvement: Tracking your job search activities allows you to identify patterns and trends. You can analyze which strategies are working well, which companies have shown interest, and which areas may require improvement. These insights help you refine your approach and increase your chances of success in future applications."
]


class ApplicationsViewSet(
                    mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   # mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet
                    ):
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]
    # serializer_class = ApplicationsSerializer


    def get_queryset(self):
        super().get_queryset()
        if not self.request.user.is_staff:
            qs = self.queryset.filter(user=self.request.user.id, is_deleted=False).prefetch_related(Prefetch('application_flows',queryset=ApplicationFlow.objects.filter(is_deleted=False)))


            return qs
        return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.request.user.is_staff:
                return ApplicationsStaffSerializer
            return ApplicationsSerializer
        else:
            return ApplicationPostSerializer

    def validate_application_exists(self):
        job_id = self.request.data['job']
        user_id= self.request.user.id
        applicatio_qs = Application.objects.filter(user=user_id,job=job_id)

        if applicatio_qs:
            raise ValidationError(
                    f"Not Unique! The job #<{job_id}> already in favorites of user <{self.request.user.username}>")

    def create_first_application_flow(self,application_data ):

        # Congratulation note
        congratulation_note = random.choice(first_notes_congratulations)
        new_application_flow = ApplicationFlow.objects.create(application_id=application_data['id'], notes = congratulation_note)

        # Explanation note
        explanation_note = random.choice(first_notes_explanations)
        new_application_flow = ApplicationFlow.objects.create(application_id=application_data['id'], notes = explanation_note)

        # Suggestion note
        suggestion_note = random.choice(first_notes_suggestions)
        new_application_flow = ApplicationFlow.objects.create(application_id=application_data['id'], notes = suggestion_note)

        # print(new_application_flow)

    def create(self, request, *args, **kwargs):

        self.validate_application_exists()
        my_request_data = copy.deepcopy(request.data)
        my_request_data['user'] = self.request.user.id

        # self.create_first_application_flow()

        serializer = self.get_serializer(data=my_request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.create_first_application_flow(application_data = serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        instance.is_deleted= True
        instance.save()

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         # for application in serializer.data:
    #         #     applicationFlows = A
    #         #     print(application)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)