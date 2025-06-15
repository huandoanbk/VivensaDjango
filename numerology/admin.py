from django.contrib import admin

# Register your models here.
from .models import NumerologyResult, NumerologyMeaning, ApiLog


@admin.register(NumerologyResult)
class NumerologyResultAdmin(admin.ModelAdmin):
    list_display = [
        'public_id', 'firstname', 'lastname', 'birthdate', 'language',
        'life_path_number', 'expression_number', 'soul_urge_number',
        'personality_number', 'attitude_number', 'natural_ability_number',
        'thinking_capacity_number', 'maturity_number'
    ]
    list_filter = ['language', 'birthdate']
    search_fields = ['public_id', 'firstname', 'lastname']
    readonly_fields = ('public_id', 'created_at')
    ordering = ('-created_at',)

@admin.register(NumerologyMeaning)
class NumerologyMeaningAdmin(admin.ModelAdmin):
    list_display = ('type', 'number', 'language', 'variant')
    search_fields = ('type', 'number', 'language')
    list_filter = ('type', 'language')
    ordering = ('type', 'number', 'language')


@admin.register(ApiLog)
class ApiLogAdmin(admin.ModelAdmin):
    list_display = ('numerology_result', 'model', 'tokens_used', 'request_time')
    search_fields = ('model', 'prompt')
    list_filter = ('model', 'request_time')
    ordering = ('-request_time',)
