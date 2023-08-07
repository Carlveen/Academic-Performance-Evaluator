from django.contrib import admin
from .models import Course, Question, Choice, Profile, Score


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_number', 'question_text', 'course', 'code_snippet')
    ordering = ('course', 'question_number')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'choice_text', 'is_correct')
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'email')

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'score', 'user', 'date')
    
class ProfileInline(admin.StackedInline):
    model = Profile
    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)





