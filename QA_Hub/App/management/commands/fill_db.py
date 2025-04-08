import random, requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from App.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike

fake = Faker()


class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient for filling the database')

    def handle(self, *args, **options):
        ratio = options['ratio']

        self.stdout.write(f'Generating {ratio} users...')
        users = [User(username=fake.unique.user_name(), email=fake.unique.email()) for _ in range(ratio)]
        User.objects.bulk_create(users)

        user_profiles = [Profile(user=user) for user in User.objects.all()]
        Profile.objects.bulk_create(user_profiles)

        self.stdout.write(f'Generating {ratio} tags...')

        url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt"
        response = requests.get(url)
        words = response.text.splitlines()
        words = random.sample(words, ratio)

        tags = [Tag(name=words[i]) for i in range(ratio)]
        Tag.objects.bulk_create(tags)

        self.stdout.write(f'Generating {ratio * 10} questions...')
        users = list(User.objects.all())
        questions = [
            Question(title=fake.sentence(), content=fake.text(), author=random.choice(users))
            for _ in range(ratio * 10)
        ]
        Question.objects.bulk_create(questions)

        questions = list(Question.objects.all())
        for question in questions:
            for _ in range(random.randint(1, 5)):
                question.tags.add(random.choice(tags))

        self.stdout.write(f'Generating {ratio * 100} answers...')
        questions = list(Question.objects.all())
        answers = [
            Answer(question=random.choice(questions), content=fake.text(), author=random.choice(users))
            for _ in range(ratio * 100)
        ]
        Answer.objects.bulk_create(answers)

        self.stdout.write(f'Generating {ratio * 200} likes...')
        answers = list(Answer.objects.all())
        questions = list(Question.objects.all())

        question_likes = []
        answer_likes = []

        used_question_pairs = set()
        used_answer_pairs = set()

        while len(question_likes) + len(answer_likes) < ratio * 200:
            user = random.choice(users)

            if random.random() > 0.5:
                question = random.choice(questions)
                pair = (user.id, question.id)
                if pair not in used_question_pairs:
                    used_question_pairs.add(pair)
                    question_likes.append(QuestionLike(user=user, question=question, is_like=True))
            else:
                answer = random.choice(answers)
                pair = (user.id, answer.id)
                if pair not in used_answer_pairs:
                    used_answer_pairs.add(pair)
                    answer_likes.append(AnswerLike(user=user, answer=answer, is_like=True))

        QuestionLike.objects.bulk_create(question_likes)
        AnswerLike.objects.bulk_create(answer_likes)

        self.stdout.write(self.style.SUCCESS('Database successfully filled!'))
