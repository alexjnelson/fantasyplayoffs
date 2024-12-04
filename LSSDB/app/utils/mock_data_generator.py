import random 

def generate_mock_data():
    # Mock live football data
    return {
        "game_id": "12345",
        "quarter": random.randint(1, 4),
        "time_remaining": f"{random.randint(0, 15)}:{random.randint(0, 59):02}",
        "team_a": {
            "name": "Eagles",
            "score": random.randint(0, 50),
            "possession": random.choice([True, False])
        },
        "team_b": {
            "name": "Patriots",
            "score": random.randint(0, 50),
            "possession": random.choice([True, False])
        },
        "last_play": random.choice(["Touchdown by Player 10", "Field Goal", "Fumble Recovery", "Interception"])
    }