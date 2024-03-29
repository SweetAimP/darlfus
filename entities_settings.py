entities = {
    "wolf" : {
        "size":32,
        "max_health": 70,
        "defense": 0,
        "initiative": 100,
        "mp": 10,
        "ap": 10,
        "spells" : {
            "bite":{
                "name" : "bite",
                "type": "dmg",
                "subtype" : {"buff": {"vampirism": 100}},
                "range": 8,
                "area": 1,
                "damage": 20,
                "ap_cost": 3,
                "max_usages": 2,
                "animations":{
                    "frames": 15,
                    "sw": "assets/entities/wolf/spells/bite/bite_sw.png",
                    "se": "assets/entities/wolf/spells/bite/bite_se.png",
                    "nw": "assets/entities/wolf/spells/bite/bite_nw.png",
                    "ne": "assets/entities/wolf/spells/bite/bite_ne.png"
                }
            },
            "howl":{
                "name" : "howl",
                "type": "dmg",
                "subtype" : {"debuff": {"defense": -10}},
                "range": 8,
                "area": 2,
                "damage": 10,
                "ap_cost": 2,
                "max_usages": 2,
                "animations":{
                    "frames": 9,
                    "sw": "assets/entities/wolf/spells/howl/howl_sw.png",
                    "se": "assets/entities/wolf/spells/howl/howl_se.png",
                    "nw": "assets/entities/wolf/spells/howl/howl_nw.png",
                    "ne": "assets/entities/wolf/spells/howl/howl_ne.png"
                }
            },
        },
        "animations": {
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
            "death" : {
                "sw": "assets/entities/wolf/death/death_sw.png",
                "se": "assets/entities/wolf/death/death_se.png",
                "nw": "assets/entities/wolf/death/death_nw.png",
                "ne": "assets/entities/wolf/death/death_ne.png"
            }
        }
    }
}