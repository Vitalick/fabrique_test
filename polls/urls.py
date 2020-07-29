from django.urls import path

from .views import PollList, PollDetail, ChoiceList, VoteCreate, QuestionList

urlpatterns = [
    path("polls/", PollList.as_view(), name="polls_list"),
    path("polls/<int:pk>/", PollDetail.as_view(), name="polls_detail"),
    path("choices/", ChoiceList.as_view(), name="choice_list"),
    path("questions/", QuestionList.as_view(), name="question_list"),
    path("vote/", VoteCreate.as_view(), name="vote_create"),
]
