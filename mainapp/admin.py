from django.contrib import admin
from .models import Chapter, Question, Resource

# Chapter Admin
@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Question Admin
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'chapter', 'correct_option')
    list_filter = ('chapter',)
    search_fields = ('question_text',)
    
admin.site.register(Resource)