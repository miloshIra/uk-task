import logging

import pokebase as pb
from django.core.cache import cache

from .models import Pokemon

logger = logging.getLogger(__name__)


def get_or_create_pokemon(*, pokemon_name: str):
    key = f"pokemon:{pokemon_name.lower()}"

    try:

        if pokemon := cache.get(key):
            return pokemon

        if pokemon := Pokemon.objects.filter(name=pokemon_name.lower()).first():
            return pokemon

        poke_data = pb.pokemon(pokemon_name.lower())

        pokemon = Pokemon.objects.create(
            name=poke_data.name,
            health=poke_data.stats[0].base_stat,
            attack=poke_data.stats[1].base_stat,
            defense=poke_data.stats[2].base_stat,
        )

        pokemon.save()
        cache.set(key, pokemon, timeout=60 * 60)

        return pokemon

    except Exception:
        raise ValueError(f"❌ Pokémon '{pokemon_name}' not found!")
