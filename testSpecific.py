from connect4 import make_rack, print_rack, place_disc
from connect4player import ComputerPlayer
import sys

def load_rack(filename):
  with open(filename) as file:
    chars = [line.split(" ") for line in file]
    rack = make_rack(len(chars[0]), len(chars))
    for r in range(len(chars)):
      for c in range(len(chars[r])):
        rack[c][-r] = 1 if chars[r][c] == "X" else 2
    return rack

rack = load_rack(sys.argv[1])
print_rack(rack)

player = ComputerPlayer(int(sys.argv[2]), int(sys.argv[3]))
move = player.pick_move(rack)
place_disc(rack, player._id, move)

print()
print_rack(rack)
