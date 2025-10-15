import requests
from flask import current_app
from typing import Optional, Dict

class PokeAPIService:
    
    @staticmethod
    def get_base_url():
        return current_app.config.get('POKEAPI_BASE_URL', 'https://pokeapi.co/api/v2')
    
    @staticmethod
    def get_pokemon_list(limit=151, offset=0):
        try:
            url = f"{PokeAPIService.get_base_url()}/pokemon"
            params = {'limit': limit, 'offset': offset}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    @staticmethod
    def get_pokemon_details(pokemon_id):
        try:
            url = f"{PokeAPIService.get_base_url()}/pokemon/{pokemon_id}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    @staticmethod
    def format_pokemon_for_frontend(pokemon_data):
        if not pokemon_data:
            return None
        
        return {
            'id': pokemon_data.get('id'),
            'name': pokemon_data.get('name'),
            'types': [t['type']['name'] for t in pokemon_data.get('types', [])],
            'sprites': pokemon_data.get('sprites', {})
        }