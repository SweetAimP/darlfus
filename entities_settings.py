entities = {
    "wolf" : {
        "size":32,
        "max_health": 250,
        "initiative": 100,
        "mp": 10,
        "ap": 10,
        "spells" :[
            {"name": "S1", "type": "dmg" ,"range":2, "area":1, "damage": 25, "ap_cost": 3, "max_usages": 2},
            {"name": "S2", "type": "mov" ,"range":8, "area":0, "damage": 0, "ap_cost": 3, "max_usages": 2}
        ],
        "assets": {
            "idle" : {
                "sw": "assets/entities/wolf/idle/idle_ne.png",
                "se": "assets/entities/wolf/idle/idle_ne.png",
                "nw": "assets/entities/wolf/idle/idle_ne.png",
                "ne": "assets/entities/wolf/idle/idle_ne.png"
            },
            "walk" : {
                "sw": "assets/entities/wolf/idle/walk_ne.png",
                "se": "assets/entities/wolf/idle/walk_ne.png",
                "nw": "assets/entities/wolf/idle/walk_ne.png",
                "ne": "assets/entities/wolf/idle/walk_ne.png"
            }
        }
    }
}