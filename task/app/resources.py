import logging
import random
import sys

import pokebase as pb
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .client import get_or_create_pokemon
from .models import Battle
from .serializers import BattleSerializer

logger = logging.getLogger(__name__)


@api_view(["GET"])
def health_check(request):
    return Response({"status": "healthy"})


class BattleViewSet(viewsets.ModelViewSet):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
    ordering = ["-created_at"]
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer()

        pokemon_one_name = str(kwargs.get("pokemon1"))
        pokemon_two_name = str(kwargs.get("pokemon2"))

        pokemon_one = get_or_create_pokemon(pokemon_name=pokemon_one_name)
        pokemon_two = get_or_create_pokemon(pokemon_name=pokemon_two_name)

        logger.info("---------The battle is about to begin!------------")
        logger.info(
            f"\n{pokemon_one.name.capitalize()} \nHP:{pokemon_one.health} ATK:{pokemon_one.attack} DEF:{pokemon_one.defense}"
        )
        logger.info("== VS ==")
        logger.info(
            f"\n{pokemon_two.name.capitalize()} \nHP:{pokemon_two.health} ATK:{pokemon_two.attack} DEF:{pokemon_two.defense}"
        )

        attacker = random.choice([pokemon_one, pokemon_two])
        defender = pokemon_two if attacker == pokemon_one else pokemon_one

        logger.info(f"\n {attacker.name.capitalize()} makes the first move!\n")

        battle_log = {}
        round_number = 1

        while attacker.health > 0 and defender.health > 0:
            base_damage = attacker.attack - defender.defense
            damage = max(1, int(base_damage * random.uniform(0.5, 1.2)))
            defender.health -= damage

            battle_log[f"Round {round_number}"] = (
                f"{attacker.name.capitalize()} attacks "
                f"{defender.name.capitalize()} for {damage} damage "
                f"(HP left: {max(0, defender.health)})"
            )
            logger.info(battle_log[f"Round {round_number}"])

            if defender.health <= 0:
                winner, loser = attacker, defender
                logger.info(
                    f"\n {winner.name.capitalize()} wins against {loser.name.capitalize()}!"
                )
                break

            attacker, defender = defender, attacker
            round_number += 1

        battle_data = {
            "log": battle_log,
            "winner": winner.name if winner else None,
            "loser": loser.name if loser else None,
        }

        serializer = self.get_serializer(data=battle_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
