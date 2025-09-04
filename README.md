## Pokemon game assiment

### This project is dockerized, to run it:

1. Clone the repo locally
2. Change the .env.example file to .env file
    - I am aware it already has data and that it's not best practice to leave it, but this is not a real project so it should be fine.

3. Set up the venv(optional)

    - I prefer running different projects in different enviroments to create a virtual enviroment use the following:

    ```
    python -m venv venv
    venv\Scripts\activate.bat
    ```
    

4. Run the project with:

```
    docker-compose -up --build
```

## Endpoints

- The app has an exposed endpoint at /battle, to use it properly and battle two pokemons you need add their names as parameters, example:

```
    /battle/pikachu/charizard/
```

I used postman to test the endpoint and I have provided the collection in the this repo so you can do that same.

## Battle algoritam

The battle algoritam is as simple as the time allows, it is turn bases and the turn order is random,
I am getting the pokemon data from pokebase.co, and I focus on 3 attributes, 
the pokemon attack, defense and health, the algoritam is as follows:

 ```
 base_damage = attacker.attack - defender.defense
 damage = max(1, int(base_damage * random.uniform(0.5, 1.2)))
 ```

The random.uniform is just a small modifier to make things more interesting and avoids an uniform outcome. 
The battle goes on as long as one of the pokemons health drops to 0, and them the battle/battle log is saved and the winner is announced. 

### Since this is only a backend project the winner is announced with a logger and in the response.