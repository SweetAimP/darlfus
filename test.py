class Spell:
    def __init__(self, name, cost, damage, max_uses):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.max_uses = max_uses
        self.remaining_uses = max_uses

def select_best_combo(spells, spell_capacity):
    memo = {}  # Dictionary to store already computed results

    def dp(current_spell, remaining_capacity):
        if current_spell < 0 or remaining_capacity == 0:
            return 0, []

        if (current_spell, remaining_capacity) in memo:
            return memo[(current_spell, remaining_capacity)]

        max_damage = 0
        best_combo = []

        # Try using the current spell
        for uses in range(min(spells[current_spell].remaining_uses, remaining_capacity // spells[current_spell].cost) + 1):
            total_damage, remaining_combos = dp(current_spell - 1, remaining_capacity - uses * spells[current_spell].cost)
            total_damage += uses * spells[current_spell].damage

            if total_damage > max_damage:
                max_damage = total_damage
                best_combo = remaining_combos + [(spells[current_spell], uses)]

        memo[(current_spell, remaining_capacity)] = max_damage, best_combo
        return max_damage, best_combo

    total_damage, selected_spells = dp(len(spells) - 1, spell_capacity)
    return total_damage, selected_spells

# Example usage:
spell1 = Spell("Spell 1", 3, 10, 2)
spell2 = Spell("Spell 2", 6, 15, 1)

enemy_spells = [spell1]
spell_capacity = 10

best_damage, selected_spells = select_best_combo(enemy_spells, spell_capacity)

if selected_spells:
    print("Best combo:")
    for spell, uses in selected_spells:
        print(f"{spell.name} x{uses}")
    print(f"Total damage: {best_damage}")
else:
    print("No valid combo within spell capacity.")
