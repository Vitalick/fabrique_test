from rest_framework import serializers

from .models import Poll, Choice, Vote, Answer, Question


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
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
    votes = VoteSerializer(many=True, read_only=True, required=False)

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
