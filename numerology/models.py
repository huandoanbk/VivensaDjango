from django.db import models

# Create your models here.

class NumerologyResult(models.Model):
    public_id = models.CharField(max_length=9, unique=True, editable=False)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100,null=True)
    birthdate = models.DateField()
    language = models.CharField(max_length=5, default='en')
    created_at = models.DateTimeField(auto_now_add=True)

    # Core numerology numbers
    life_path_number = models.CharField(max_length=5, null=True, blank=True)
    expression_number = models.CharField(max_length=5, null=True, blank=True)
    soul_urge_number = models.CharField(max_length=5, null=True, blank=True)
    personality_number = models.CharField(max_length=5, null=True, blank=True)
    attitude_number = models.CharField(max_length=5, null=True, blank=True)
    natural_ability_number = models.CharField(max_length=5, null=True, blank=True)
    thinking_capacity_number = models.CharField(max_length=5, null=True, blank=True)
    maturity_number = models.CharField(max_length=5, null=True, blank=True)

    karmic_numbers = models.JSONField(default=list, null=True, blank=True)
    birthday_chart = models.JSONField(default=dict, null=True, blank=True)
    pyramid_chart = models.JSONField(default=dict, null=True, blank=True)

    # AI-generated content
    ai_generated_intro = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} ({self.public_id})"


class NumerologyMeaning(models.Model):
    TYPE_CHOICES = [
        ('LIFE_PATH', 'Life Path'),
        ('EXPRESSION', 'Expression'),
        ('SOUL_URGE', 'Soul Urge'),
        ('PERSONALITY', 'Personality'),
        ('ATTITUDE', 'Attitude'),
        ('NATURAL_ABILITY', 'Natural Ability'),
        ('THINKING_CAPACITY', 'Thinking Capacity'),
        ('MATURITY', 'Maturity'),
        ('KARMIC_NUMBERS', 'Karmic Numbers'),
        ('BIRTHDAY_CHART', 'Birthday Chart'),
        ('PERSONAL_YEAR', 'Personal Year Cycle'),
        ('PYRAMID', 'Pyramid'),
    ]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    number = models.CharField(max_length=10)  # e.g. '3', '13,14', 'GENERAL'
    language = models.CharField(max_length=5)
    variant = models.IntegerField(default=1)
    content = models.TextField()

    class Meta:
        unique_together = ('type', 'number', 'language', 'variant')

    def __str__(self):
        return f"{self.type} {self.number} ({self.language})"


class ApiLog(models.Model):
    numerology_result = models.ForeignKey(NumerologyResult, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)
    prompt = models.TextField()
    response = models.TextField()
    tokens_used = models.IntegerField()
    model = models.CharField(max_length=50)

    def __str__(self):
        return f"Log {self.model} ({self.request_time})"
