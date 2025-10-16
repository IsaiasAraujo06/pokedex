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
            current_app.logger.error(f"Error fetching pokemon list: {e}")
            return None
    
    @staticmethod
    def get_pokemon_details(pokemon_id):
        try:
            url = f"{PokeAPIService.get_base_url()}/pokemon/{pokemon_id}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error fetching pokemon {pokemon_id}: {e}")
            return None
    
    @staticmethod
    def get_pokemon_by_name(name):
        """Busca Pokémon pelo nome"""
        try:
            url = f"{PokeAPIService.get_base_url()}/pokemon/{name.lower()}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error fetching pokemon {name}: {e}")
            return None
    
    @staticmethod
    def get_generation(generation_id):
        """Busca informações de uma geração específica"""
        try:
            url = f"{PokeAPIService.get_base_url()}/generation/{generation_id}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error fetching generation {generation_id}: {e}")
            return None
    
    @staticmethod
    def format_pokemon_for_frontend(pokemon_data):
        if not pokemon_data:
            return None
        
        return {
            'id': pokemon_data.get('id'),
            'name': pokemon_data.get('name'),
            'height': pokemon_data.get('height'),
            'weight': pokemon_data.get('weight'),
            'types': [t['type']['name'] for t in pokemon_data.get('types', [])],
            'abilities': [a['ability']['name'] for a in pokemon_data.get('abilities', [])],
            'stats': {
                stat['stat']['name']: stat['base_stat'] 
                for stat in pokemon_data.get('stats', [])
            },
            'sprites': {
                'front_default': pokemon_data.get('sprites', {}).get('front_default'),
                'front_shiny': pokemon_data.get('sprites', {}).get('front_shiny'),
                'official_artwork': pokemon_data.get('sprites', {}).get('other', {}).get('official-artwork', {}).get('front_default')
            }
        }