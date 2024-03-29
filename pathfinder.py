from queue import PriorityQueue
from utils import *

class PathFinder:
    def __init__(self):
        self.reconstructed_path = []
        self.movement_direction = []
        self.start = None
        self.end = None

    def _reset_variables(self):
        self.reconstructed_path = []
        self.movement_direction = []
        self.start = None
        self.end = None

    def _h(self, p1,p2):
        x1,y1 = p1
        x2,y2 = p2             
        return abs(x1 - x2) + abs(y1 - y2)

    def _reconstruct_path(self,came_from, current):
        while current in came_from:
            current = came_from[current]
            self.reconstructed_path.append(current)

    def _get_reconstructed_path_directions(self,end):
        for index, step in enumerate(self.reconstructed_path):
            if step != end:
                self.movement_direction.append(
                    check_facing(
                        self.reconstructed_path[index+1].grid_pos,
                        step.grid_pos
                        )
                )
        self.movement_direction.append(self.movement_direction[-1])

    def find_path(self, grid, start, end, caller):
            self.start = start
            self.end = end
            count = 0
            open_set = PriorityQueue()
            open_set.put((0, count, start))
            came_from = {}
            g_score = {spot: float("inf") for row in grid for spot in row}
            g_score[start] = 0
            f_score = {spot: float("inf") for row in grid for spot in row}
            f_score[start] = self._h(start.get_pos(), end.get_pos())
            open_set_hash = {start}
            
            while not open_set.empty():
                current = open_set.get()[2]
                open_set_hash.remove(current)
                if current == end:
                    self._reconstruct_path(came_from, end)
                    self.reconstructed_path = self.reconstructed_path[::-1]
                    self.reconstructed_path.append(end)
                    self._get_reconstructed_path_directions(end)
                    reconstructed_path = self.reconstructed_path[1::]
                    movement_direction = self.movement_direction
                    self._reset_variables()
                    return reconstructed_path,movement_direction
                               
                for neighbor in current.neighbors:
                    if caller.tag == 'player':
                        if neighbor.walkable:
                            self._get_score(g_score,f_score,came_from,current,open_set_hash,neighbor,end,open_set,count)
                    elif caller.tag == 'npc':
                        if not neighbor.walkable and neighbor.status == 2 and neighbor == end:
                            self._get_score(g_score,f_score,came_from,current,open_set_hash,neighbor,end,open_set,count)
                        elif neighbor.walkable:
                            self._get_score(g_score,f_score,came_from,current,open_set_hash,neighbor,end,open_set,count)
            return False
    
    def _get_score(self,g_score,f_score,came_from,current,open_set_hash,neighbor,end,open_set,count):
        temp_g_score = g_score[current] + 1
        if temp_g_score < g_score[neighbor]:
            came_from[neighbor] = current
            g_score[neighbor] = temp_g_score
            f_score[neighbor] = temp_g_score + self._h(neighbor.get_pos(), end.get_pos())
            if neighbor not in open_set_hash:
                count += 1
                open_set.put((f_score[neighbor], count, neighbor))
                open_set_hash.add(neighbor)