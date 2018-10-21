from poll.models import Question


def polls_count(request):
    count = Question.objects.count()
    return {"polls_count": count}
