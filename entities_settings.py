entities = {
    "warrior" : {
        "size":32,
        "max_health": 250,
        "initiative": 100,
        "mp": 16,
        "ap": 10,
        "spells" :[
            {"type": "dmg" ,"range":2, "area":1, "damage": 35, "ap_cost": 3},
            {"type": "mov" ,"range":8, "area":0, "damage": 0, "ap_cost": 3}
        ],
    },
    "archer" : {
        "size":32,
        "max_health": 185,
        "initiative": 120,
        "mp": 16,
        "ap": 10,
        "spells" :[
            {"type": "dmg", "range":10, "area":0, "damage": 15, "ap_cost": 5},
            {"type": "dmg", "range":8, "area":2, "damage": 8, "ap_cost": 3},
            {"type": "dmg", "range":7, "area":5, "damage": 8, "ap_cost": 2}
        ],
    }
}