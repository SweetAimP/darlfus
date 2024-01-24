entities = {
    "wolf" : {
        "size":32,
        "max_health": 70,
        "initiative": 100,
        "mp": 10,
        "ap": 10,
        "spells" :[
            {"name": "S1", "type": "dmg" ,"range":2, "area":1, "damage": 25, "ap_cost": 3, "max_usages": 2},
            {"name": "S2", "type": "mov" ,"range":8, "area":0, "damage": 0, "ap_cost": 3, "max_usages": 2}
        ],
        "assets": {
            "idle" : {
                "sw": "assets/entities/wolf/idle/idle_sw.png",
                "se": "assets/entities/wolf/idle/idle_se.png",
                "nw": "assets/entities/wolf/idle/idle_nw.png",
                "ne": "assets/entities/wolf/idle/idle_ne.png"
            },
            "walk" : {
                "sw": "assets/entities/wolf/walk/walk_sw.png",
                "se": "assets/entities/wolf/walk/walk_se.png",
                "nw": "assets/entities/wolf/walk/walk_nw.png",
                "ne": "assets/entities/wolf/walk/walk_ne.png"
            },
            "attack" : {
                "sw": "assets/entities/wolf/attack/attack_sw.png",
                "se": "assets/entities/wolf/attack/attack_se.png",
                "nw": "assets/entities/wolf/attack/attack_nw.png",
                "ne": "assets/entities/wolf/attack/attack_ne.png"
            }
        }
    }
}