from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User


QUESTION_TYPES = (
    ('multiple_choice', 'Multiple Choice'),
    ('true_false', 'True/False'),
    ('short_answer', 'Short Answer'),
)


# Create your models here.
# In your models.py file



class Course(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    code_snippet = models.TextField(blank=True, null=True)
    question_number = models.IntegerField(default=0)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)

    def __str__(self):
         return f"{self.question_number}. {self.question_text} \n Code Snippet: {self.code_snippet} \n Correct Answer: {self.choice_set.get(is_correct=True).choice_text}"



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    code_snippet = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.choice_text
    
       
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True)
    programming_in_c_score = models.IntegerField(default=0)

    def get_percentage_score(self, course_id):
        # check if the score is already cached
        cache_key = f'course_{course_id}_user_{self.user.id}_score'
        percentage_score = cache.get(cache_key)
        if percentage_score is not None:
            return percentage_score

        # calculate the score if not cached
        try:
            course = Course.objects.get(id=course_id)
            latest_score = Score.objects.filter(course=course, user=self.user).order_by('-date').first()
            if latest_score:
                total_questions = course.question_set.count()
                percentage_score = int((latest_score.score / total_questions) * 100)

                # create a new Score object with the calculated percentage score
                score = Score.objects.create(course=course, score=percentage_score, user=self.user)

                # cache the score for future use
                cache.set(cache_key, percentage_score)

                return percentage_score
        except:
            pass

        return 0

    
class Score(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course} - {self.score} ({self.user})"
    
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num_correct = models.PositiveIntegerField()
    num_questions = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.course} ({self.num_correct}/{self.num_questions})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a Score object for the user
        score = Score.objects.create(course=self.course, user=self.user, score=self.num_correct, date=self.date)
        score.save()

