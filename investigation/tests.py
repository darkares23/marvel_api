import pytest
import responses
from django.test import TestCase
from django.urls import reverse

from .manager import get_marvel_character
from .models import Character


# Manager tests
class ManagerTests(TestCase):
    @responses.activate
    def test_get_marvel_character(self):
        # Use a valid character name from the Marvel API
        character_name = "Spider-Man"

        # Mock API response data
        mock_response = {
            "data": {
                "results": [
                    {
                        "id": 123,
                        "name": "Spider-Man",
                        "description": "Friendly neighborhood Spider-Man",
                        "thumbnail": {
                            "path": "https://example.com/image",
                            "extension": "jpg",
                        },
                    }
                ]
            }
        }

        # Mock the Marvel API endpoint
        responses.add(
            responses.GET,
            "https://gateway.marvel.com/v1/public/characters",
            json=mock_response,
            status=200,
        )

        character_data = get_marvel_character(character_name)

        # Verify the returned data contains the expected fields
        self.assertIn("id", character_data)
        self.assertIn("name", character_data)
        self.assertIn("description", character_data)
        self.assertIn("thumbnail", character_data)

        # Verify the returned character name matches the input
        self.assertEqual(character_data["name"], character_name)


# Model tests
class CharacterModelTests(TestCase):
    def test_character_creation(self):
        character = Character.objects.create(
            id=123,
            marvel_id=123,
            name="Test Character",
            description="Test Description",
            thumbnail="https://example.com/image.jpg",
        )
        self.assertEqual(character.name, "Test Character")
        self.assertEqual(character.description, "Test Description")
        self.assertEqual(character.thumbnail, "https://example.com/image.jpg")


# View tests
class CharacterViewTests(TestCase):
    def test_populate_view(self):
        url = reverse("populate")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @pytest.mark.xfail
    def test_characters_view(self):
        url = reverse("characters")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @pytest.mark.xfail
    def test_character_view(self):
        # Create a test character in the database
        character = Character.objects.create(
            id=123,
            marvel_id=123,
            name="Test Character",
            description="Test Description",
            thumbnail="https://example.com/image.jpg",
        )
        url = reverse("character", args=[character.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Character")

    @pytest.mark.xfail
    def test_delete_character_view(self):
        # Deletes a test character in the database
        character = Character.objects.create(
            id=123,
            marvel_id=123,
            name="Test Character",
            description="Test Description",
            thumbnail="https://example.com/image.jpg",
        )
        url = reverse("delete_character", args=[character.name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Character.objects.filter(id=123).exists())
