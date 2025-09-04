import uuid

from django.db import models
from django.db.models import JSONField


class Battle(models.Model):
    """
    Represents a Pokemon battle between two combatants.

    fields:
        id (UUIDField): Primary key, auto-generated UUID for unique identification
        winner (CharField): Name of the winning Pokemon (optional)
        loser (CharField): Name of the losing Pokemon (optional)
        log (JSONField): Detailed battle log containing round-by-round actions
        created_at (DateTimeField): Timestamp when the battle was created
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    winner = models.CharField(max_length=200, null=True, blank=True)
    loser = models.CharField(max_length=200, null=True, blank=True)
    log = JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Battle id {self.id}, winner {self.winner}, loser {self.loser}"

    class Meta:
        indexes = [
            models.Index(fields=["created_at", "id"], name="created_uuid_idx"),
        ]


class Pokemon(models.Model):
    """
    Represents a Pokémon creature with basic stats.

    fields:
        id (UUIDField): Unique identifier for the Pokémon (primary key).
        name (CharField): Name of the Pokémon. Indexed for fast lookups.
        health (IntegerField): Health points of the Pokémon.
        attack (IntegerField): Attack power of the Pokémon.
        defense (IntegerField): Defense power of the Pokémon.
    """

    name = models.CharField(max_length=200, null=True, blank=True)
    health = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["name"], name="pokemon_name_idx"),
        ]
