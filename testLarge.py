from connect4player import ComputerPlayer
from connect4 import make_rack, place_disc, print_rack, find_win, P1_ESCAPE, P2_ESCAPE, END_ESCAPE

player1 = ComputerPlayer(1, 4)
player2 = ComputerPlayer(2, 4)
player1._prune = True
player2._prune = True
rack = make_rack(13, 8)
current_player = 1
winning_quartet = None

while not winning_quartet:
  current_player = 3 - current_player
  move = -1
  if current_player == 1:
    move = player1.pick_move(rack)
  else:
    move = player2.pick_move(rack)
  place_disc(rack, current_player, move)
  winning_quartet = find_win(rack, move)

print_rack(rack)
