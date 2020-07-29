from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Poll, Question, Choice, Vote, Answer
from .serializers import PollSerializer, QuestionSerializer, VoteSerializer, ChoiceSerializer, PollSerializerUpdate, \
    UserSerializer


class PollList(generics.ListCreateAPIView):
    serializer_class = PollSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Poll.objects.all()
        else:
            return Poll.objects.filter(start_date__lt=now(), finish_date__gt=now())


class PollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializerUpdate


class QuestionList(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetail(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceList(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class VoteCreate(generics.CreateAPIView):
    serializer_class = VoteSerializer

    def post(self, request, *args, **kwargs):
        try:
            poll = request.data['poll']
            poll = Poll.objects.get(id=poll)
        except:
            return Response({'error': 'Enter right poll!'})
        if not poll.is_active():
            return Response({'error': 'Enter active poll!'})
        try:
            voted_by = request.data['voted_by']
        except:
            return Response({'error': 'Enter voted_by!'})
        try:
            answers = request.data['answers']
        except:
            return Response({'error': 'Enter answers!'})
        for answer in answers:
            question_in_answer = Question.objects.get(id=answer['question'])
            if question_in_answer.poll != poll:
                return Response({'error': f'Question {question_in_answer.id} not in poll {poll.id}!'})
            if not ((question_in_answer.type == 'text' and len(answer['text']) > 0) or
                    (question_in_answer.type == 'single' and len(answer['choices']) == 1) or
                    (question_in_answer.type == 'multi' and len(answer['choices']) > 0)):
                return Response({'error': f'Answer for question {answer["question"]} wrong!'})
        try:
            vote = Vote.objects.get(poll=poll, voted_by=voted_by)
            if len(vote.answers.all()) == len(poll.questions.all()):
                return Response({'error': f'User already voted on this poll'})
        except:
            vote = Vote(poll=poll, voted_by=voted_by)
            try:
                vote.save()
            except Exception as e:
                return Response({'error': f'User already voted on this poll ({e})'})
        if len(answers) < len(poll.questions.all()):
            return Response({'error': f'Not enough answers ({len(answers)} < {len(poll.questions)})'})
        for answer in answers:
            question_in_answer = Question.objects.get(id=answer['question'])
            answer_db = Answer(vote=vote, question=question_in_answer)
            try:
                answer_db.save()
            except Exception as e:
                return Response({'error': f'Error with answer save ({e})'})
            if question_in_answer.type == 'text':
                answer_db.text = answer.get('text', '')
            else:
                for choice in Choice.objects.filter(id__in=answer.get('choices', [])):
                    answer_db.choices.add(choice)
            try:
                answer_db.save()
            except Exception as e:
                return Response({'error': f'Error with answer save 2 ({e})'})
        return redirect(vote)


class VoteDetail(generics.RetrieveDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)