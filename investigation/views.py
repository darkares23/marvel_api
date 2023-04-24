import csv

from celery import chain
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics

from .manager import create_related_characters_in_database, create_spectrum_in_database
from .models import Character


def populate(request):
    try:
        # Create a task chain
        task_chain = chain(create_spectrum_in_database.s(), create_related_characters_in_database.s())
        task_chain.apply_async()
        return HttpResponse("Database populated successfully")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


def all_characters(request):
    characters = Character.objects.all()
    characters_serialized = serializers.serialize("json", characters)
    return JsonResponse(characters_serialized, safe=False)


def export_characters_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="characters.csv"'

    writer = csv.writer(response)
    writer.writerow(["id", "name", "description", "thumbnail"])

    characters = Character.objects.all().values_list("id", "name", "description", "thumbnail")
    for character in characters:
        writer.writerow(character)

    return response


def character_detail(request, character_id):
    try:
        character = Character.objects.get(marvel_id=character_id)
        character_serialized = serializers.serialize("json", [character])
    except Character.DoesNotExist:
        return JsonResponse({"error": "Character not found"}, status=404)

    return JsonResponse(character_serialized, safe=False)


@csrf_exempt
def delete_character_by_name(request):
    if request.method == "DELETE":
        character_name = request.GET.get("name", None)
        if character_name is None:
            return JsonResponse({"error": "Name parameter is missing"}, status=400)

        try:
            character = Character.objects.get(name=character_name)
            character.delete()
            return JsonResponse({"success": f"Character '{character_name}' deleted"}, status=200)
        except Character.DoesNotExist:
            return JsonResponse({"error": "Character not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
