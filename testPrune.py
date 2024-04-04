from connect4player import ComputerPlayer
from connect4 import make_rack, exists_legal_move, place_disc, find_win, print_rack, do_human_turn

player11 = ComputerPlayer(1, 4)
player21 = ComputerPlayer(1, 4)
player12 = ComputerPlayer(2, 4)
player22 = ComputerPlayer(2, 4)

player11._prune = False
player21._prune = False
player12._prune = False
player22._prune = True

rack1 = make_rack(13, 8)
rack2 = make_rack(13, 8)
current_player = 2

winning_quartet = None

while not winning_quartet:
  current_player = 3 - current_player

  if not exists_legal_move(rack1) or not exists_legal_move(rack2): break

  move1 = -1
  move2 = -1
  if current_player == 1:
    move1 = player11.pick_move(rack1)
    move2 = player21.pick_move(rack2)
    # print_rack(rack1)
    # move1 = move2 = do_human_turn(rack1, current_player)
  else:
    move1 = player12.pick_move(rack1)
    move2 = player22.pick_move(rack2)

  assert move1 == move2

  place_disc(rack1, current_player, move1)
  place_disc(rack2, current_player, move2)

  assert rack1 == rack2

  winning_quartet = find_win(rack1, move1)
  if not winning_quartet:
    winning_quartet = find_win(rack2, move2)

print("Finished!")
print()
print_rack(rack1)
print()
print_rack(rack2)
