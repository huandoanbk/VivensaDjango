from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from .serializers import NumerologyRequestSerializer
from .utils import (
    calculate_life_path, calculate_expression_number,
    calculate_soul_urge_number, calculate_personality_number,
    calculate_attitude_number, calculate_natural_ability_number,
    calculate_thinking_capacity_number,
    get_meaning, generate_azure_intro, generate_unique_public_id
)
from .models import NumerologyResult, ApiLog

@api_view(['POST'])
def numerology_full_analysis(request):
    serializer = NumerologyRequestSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        firstname = data['firstname']
        lastname = data['lastname']
        birthdate = data['birthdate']
        language = data['language']

        karmic_log = set()

        life_path = calculate_life_path(birthdate, karmic_log)
        expression = calculate_expression_number(firstname, lastname, karmic_log)
        soul_urge = calculate_soul_urge_number(firstname, lastname, karmic_log)
        personality = calculate_personality_number(firstname, lastname, karmic_log)
        attitude = calculate_attitude_number(birthdate)
        natural_ability = calculate_natural_ability_number(birthdate, karmic_log)
        thinking_capacity = calculate_thinking_capacity_number(firstname)
        # maturity = calculate_maturity_number(life_path, expression)
        # personal_year = calculate_personal_years(birthdate)
        ai_data = generate_azure_intro(f"{firstname} {lastname}", birthdate, language,life_path)
        # pyramid_chart = calculate_pyramid_chart(birthdate)
        ai_intro = ai_data["intro"]


        result = NumerologyResult.objects.create(
            public_id=generate_unique_public_id(),
            firstname=firstname,
            lastname=lastname,
            birthdate=birthdate,
            language=language,
            life_path_number=life_path,
            expression_number=expression,
            soul_urge_number=soul_urge,
            personality_number=personality,
            attitude_number=attitude,
            natural_ability_number=natural_ability,
            thinking_capacity_number=thinking_capacity,
            # maturity_number=maturity,
             karmic_numbers=sorted(karmic_log),
            # pyramid_chart=pyramid_chart,
            ai_generated_intro=ai_intro
        )
        ApiLog.objects.create(
            numerology_result=result,
            prompt=ai_data["prompt"],
            response=ai_data["response"],
            tokens_used=ai_data["tokens_used"],
            model=ai_data["model"]
        )

        response_data = {
            "public_id": result.public_id,
            "firstname": firstname,
            "lastname": lastname,
            "birthdate": birthdate,
            "ai_intro": ai_intro,
            "life_path": {"value": life_path, "meaning": get_meaning('LIFE_PATH', str(life_path), language)},
            "expression_number": {"value": expression, "meaning": get_meaning('EXPRESSION', str(expression), language)},
            "soul_urge_number": {"value": soul_urge, "meaning": get_meaning('SOUL_URGE', str(soul_urge), language)},
            "personality_number": {"value": personality, "meaning": get_meaning('PERSONALITY', str(personality), language)},
            "attitude_number": {"value": attitude, "meaning": get_meaning('ATTITUDE', str(attitude), language)},
            "natural_ability_number": {"value": natural_ability, "meaning": get_meaning('NATURAL_ABILITY', str(natural_ability), language)},
            "thinking_capacity_number": {"value": thinking_capacity, "meaning": get_meaning('THINKING_CAPACITY', str(thinking_capacity), language)},
        }

        return Response(response_data, status=201)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_numerology_report(request, public_id):
    try:
        result = NumerologyResult.objects.get(public_id=public_id)
        language = result.language

        response_data = {
            "public_id": result.public_id,
            "firstname": result.firstname,
            "lastname": result.lastname,
            "birthdate": result.birthdate,
            "ai_intro": result.ai_generated_intro,
            "life_path": {"value": result.life_path_number, "meaning": get_meaning('LIFE_PATH', str(result.life_path_number), language)},
            "expression_number": {"value": result.expression_number, "meaning": get_meaning('EXPRESSION', str(result.expression_number), language)},
            "soul_urge_number": {"value": result.soul_urge_number, "meaning": get_meaning('SOUL_URGE', str(result.soul_urge_number), language)},
            "personality_number": {"value": result.personality_number, "meaning": get_meaning('PERSONALITY', str(result.personality_number), language)},
            "attitude_number": {"value": result.attitude_number, "meaning": get_meaning('ATTITUDE', str(result.attitude_number), language)},
            "natural_ability_number": {"value": result.natural_ability_number, "meaning": get_meaning('NATURAL_ABILITY', str(result.natural_ability_number), language)},
            "thinking_capacity_number": {"value": result.thinking_capacity_number, "meaning": get_meaning('THINKING_CAPACITY', str(result.thinking_capacity_number), language)},
            "karmic_numbers": {"value": result.karmic_numbers, "meaning": get_meaning('KARMIC_NUMBERS', ','.join(map(str, result.karmic_numbers)) or 'NONE', language)}        }

        return Response(response_data, status=200)

    except NumerologyResult.DoesNotExist:
        return Response({"error": "Report not found"}, status=404)
