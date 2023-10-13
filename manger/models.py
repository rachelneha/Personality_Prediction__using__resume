from typing import Optional

import json

import PyPDF2
import spacy
from django.conf import settings
from django.db import models

from ml.extractpdf import ResumeParser


class Resume(models.Model):
    resume = models.FileField(verbose_name="Upload your resume")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25, choices=[
        ("NEW", "NEW"),
        ("PROCESSED", "PROCESSED"),
        ("COMPLETED", "COMPLETED"),
        ("ERRRORED", "ERRRORED"),

    ], default="NEW")
    response = models.TextField(null=True, blank=True)
    fullname = models.CharField(max_length=200, null=True, blank=False)
    address = models.CharField(max_length=200, null=True, blank=False)
    mobile = models.CharField(max_length=200, null=True, blank=False)
    skills = models.CharField(max_length=200, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False)

    # openess = models.PositiveSmallIntegerField(default=5, verbose_name="Enjoying new experience or thing. ")
    # neurotisum = models.PositiveSmallIntegerField(default=5, verbose_name="How often you feel negativity. ")
    # conscientiousness = models.PositiveSmallIntegerField(default=5, verbose_name="Wishing to do ones work well.")
    # agreeableness = models.PositiveSmallIntegerField(default=5, verbose_name="How much would you like to work with your peers.")
    # extraversion = models.PositiveSmallIntegerField(default=5, verbose_name="How outgoing and social interaction do you like.")

    q1 = models.CharField(max_length=100, verbose_name="Question 1", choices=(
        ["Hold a team meeting to discuss the situation and come up with a new plan of action", 'Hold a team meeting to discuss the situation and come up with a new plan of action'],
        ['Break down the project into smaller, achievable tasks to boost morale and productivity', 'Break down the project into smaller, achievable tasks to boost morale and productivity'],
        ['Delegate some responsibilities to team members to share the workload.', 'Delegate some responsibilities to team members to share the workload.'],
        ['Take a step back, prioritize tasks, and focus on what\'s most important to meet the deadline.', 'Take a step back, prioritize tasks, and focus on what\'s most important to meet the deadline.'],
    ), null=True)
    q2 = models.CharField(max_length=100, verbose_name="Question 2", choices=(
        ('Embrace the nervousness and push through the discomfort to network and make new connections.', 'Embrace the nervousness and push through the discomfort to network and make new connections.'),
        ('Plan ahead by researching attendees and identifying potential conversation starters.', 'Plan ahead by researching attendees and identifying potential conversation starters.'),
        ('Start with people who seem approachable and ease into more challenging conversations.', 'Start with people who seem approachable and ease into more challenging conversations.'),
        ('Take breaks when needed to recharge and reflect on the interactions', 'Take breaks when needed to recharge and reflect on the interactions'),
    ), null=True)
    q3 = models.CharField(max_length=100, verbose_name="Question 3", choices=[
        ('Analyze the interview experience to identify areas for improvement and take action', 'Analyze the interview experience to identify areas for improvement and take action'),
        ('Focus on the positive aspects of the interview and move on from the disappointment', 'Focus on the positive aspects of the interview and move on from the disappointment'),
        ('Reach out to the interviewer for feedback and constructive criticism', 'Reach out to the interviewer for feedback and constructive criticism'),
        ('Allow yourself to feel disappointed, but then use it as motivation to pursue other opportunities', 'Allow yourself to feel disappointed, but then use it as motivation to pursue other opportunities'),
    ], null=True)
    q4 = models.CharField(max_length=120, verbose_name="Question 4", choices=(
        ('Reflect on what went wrong and identify areas for improvement for future projects', 'Reflect on what went wrong and identify areas for improvement for future projects'),
        ('Reach out to colleagues or mentors for advice and guidance', 'Reach out to colleagues or mentors for advice and guidance'),
        ('Take ownership of the failure and use it as a learning experience', 'Take ownership of the failure and use it as a learning experience'),
        ('Focus on the successes and achievements made throughout the project', 'Focus on the successes and achievements made throughout the project'),
    ), null=True)
    q5 = models.CharField(max_length=120, verbose_name="Question 5", choices=(
        ('Use visuals and analogies to explain complex ideas in a more tangible way.', 'Use visuals and analogies to explain complex ideas in a more tangible way.'),
        ('Ask questions to gauge the other person\'s understanding and adjust communication accordingly', 'Ask questions to gauge the other person\'s understanding and adjust communication accordingly'),
        ('Provide clear and concise explanations without overwhelming the other person with too much information', 'Provide clear and concise explanations without overwhelming the other person with too much information'),
        ('Allow time for the other person to process and ask follow-up questions as needed', 'Allow time for the other person to process and ask follow-up questions as needed'),
    ), null=True)

    q6 = models.CharField(max_length=120, verbose_name="Question 6", choices=(
        ('Brainstorm potential solutions with the team and weigh the pros and cons of each option.', 'Brainstorm potential solutions with the team and weigh the pros and cons of each option.'),
        ('Identify the root cause of the problem and work towards a long-term solution.', 'Identify the root cause of the problem and work towards a long-term solution.'),
        ('Utilize past experiences and similar situations to guide decision making.', 'Utilize past experiences and similar situations to guide decision making.'),
        ('Prioritize the most urgent aspects of the problem and take action quickly to mitigate any negative impact.', 'Prioritize the most urgent aspects of the problem and take action quickly to mitigate any negative impact.'),
    ), null=True)

    gender = models.PositiveSmallIntegerField(default=0, choices=[
        (0, "FEMALE"),
        (1, "MALE"),
    ])
    age = models.PositiveSmallIntegerField(default=22)

    @property
    def predicted_data(self) -> Optional[dict]:
        try:
            if self.response:
                return json.loads(self.response)
        except Exception as e:
            pass

    @property
    def predicted_personality(self):
        if self.predicted_data:
            return self.predicted_data['predicted_personality']

    def get_personality_values(self):
        pr = ResumeParser(self.resume.path)
        return pr.get_traits()




















