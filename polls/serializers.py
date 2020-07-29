from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Poll, Choice, Vote, Answer, Question


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=True)

    class Meta:
        model = Vote
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)
    answers = AnswerSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)
    votes = VoteSerializer(many=True, read_only=True, required=False, )

    class Meta:
        model = Poll
        fields = '__all__'


class PollSerializerUpdate(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)
    votes = VoteSerializer(many=True, read_only=True, required=False)
    start_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'
