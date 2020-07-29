from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

ANSWER_TYPES = [
    ('text', 'Text answer'),
    ('single', 'Single choice'),
    ('multi', 'Multi choice'),
]


class Poll(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.title

    def is_active(self):
        if self.start_date < now() < self.finish_date:
            return True
        return False


class Vote(models.Model):
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    voted_by = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.poll} - {self.voted_by}'

    def get_absolute_url(self):
        return reverse('vote_detail', kwargs={'pk': self.id})

    class Meta:
        unique_together = ('poll', 'voted_by')


class Question(models.Model):
    poll = models.ForeignKey('Poll', related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=ANSWER_TYPES)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey('Question', related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Answer(models.Model):
    choices = models.ManyToManyField('Choice', related_name='answers', blank=True)
    text = models.CharField(max_length=200, blank=True)
    question = models.ForeignKey('Question', related_name='answers', on_delete=models.CASCADE)
    vote = models.ForeignKey('Vote', related_name='answers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'vote')

    def __str__(self):
        if self.question.type == 'text':
            return f'{self.question.text} - {self.text}'
        else:
            return f'{self.question.text} - choices'
