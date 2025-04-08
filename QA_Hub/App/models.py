from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class TagManager(models.Manager):
    def top_tags(self):
        return self.annotate(question_count=models.Count('questions')).order_by('-question_count')[:10]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def best_questions(self):
        return self.annotate(
            like_count=models.Count('question_likes', filter=models.Q(question_likes__is_like=True))).order_by(
            '-like_count')

    def new_questions(self):
        return self.order_by('-created_at')


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer by {self.author.username}"


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_likes')
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{'Like' if self.is_like else 'Dislike'} by {self.user.username} on {self.question.title}"


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_likes')
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"{'Like' if self.is_like else 'Dislike'} by {self.user.username} on Answer {self.answer.id}"
