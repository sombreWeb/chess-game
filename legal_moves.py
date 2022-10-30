# fen_dict = {'Q': 1, 'K': 2, 'R': 3, 'B': 4, 'N': 5, 'P': 6, 'q': 7, 'k': 8, 'r': 9, 'b': 10, 'n': 11, 'p': 12}
class LegalMoves:

    def __init__(self):

        self.black_pieces = {7, 8, 9, 10, 11, 12}
        self.white_pieces = {1, 2, 3, 4, 5, 6}

    def find_legal_rook_moves(self, p_memory, index):

        legal_moves = []

        if p_memory[index] == 3 or p_memory[index] == 9:

            file = index % 8
            rank = index // 8

            all_rook_moves = {x for x in range(64) if x % 8 == file or x // 8 == rank}
            directions = {1, -1, 8, -8}

            if p_memory[index] in self.white_pieces:
                own_pieces = self.white_pieces
                opp_pieces = self.black_pieces
            else:
                own_pieces = self.black_pieces
                opp_pieces = self.white_pieces

            for x in directions:
                square_counter = 1
                while True:
                    test_square_index = index + (x * square_counter)
                    if test_square_index in all_rook_moves:
                        if p_memory[test_square_index] not in own_pieces:
                            legal_moves.append(test_square_index)
                            square_counter += 1
                            if p_memory[test_square_index] in opp_pieces: break
                            continue
                        else:
                            break
                    else:
                        break

        return legal_moves

    def find_legal_bishop_moves(self, p_memory, index):

        legal_moves = []

        if p_memory[index] == 4 or p_memory[index] == 10:

            file = index % 8
            rank = index // 8

            all_bishop_moves = []
            for x in range(64):
                if x % 9 == index % 9 and x % 8 > file and x // 8 > rank:
                    all_bishop_moves.append(x)
                if x % 7 == index % 7 and x % 8 < file and x // 8 > rank:
                    all_bishop_moves.append(x)
                if x % -9 == index % -9 and x % 8 < file and x // 8 < rank:
                    all_bishop_moves.append(x)
                if x % -7 == index % -7 and x % 8 > file and x // 8 < rank:
                    all_bishop_moves.append(x)

            directions = {9, -9, 7, -7}

            if p_memory[index] in self.white_pieces:
                own_pieces = self.white_pieces
                opp_pieces = self.black_pieces
            else:
                own_pieces = self.black_pieces
                opp_pieces = self.white_pieces

            for x in directions:
                square_counter = 1
                while True:
                    test_square_index = index + (x * square_counter)
                    if test_square_index in all_bishop_moves:
                        if p_memory[test_square_index] not in own_pieces:
                            legal_moves.append(test_square_index)
                            square_counter += 1
                            if p_memory[test_square_index] in opp_pieces: break
                            continue
                        else:
                            break
                    else:
                        break

        return legal_moves

    def find_legal_knight_moves(self, p_memory, index):

        legal_moves = []

        if p_memory[index] == 5 or p_memory[index] == 11:

            file = index % 8
            rank = index // 8

            directions = {-6, -10, -15, -17, 6, 10, 15, 17}
            all_knight_moves = {index + x for x in directions if (index + x) in range(64) and (
                    abs(file - ((index + x) % 8)) + abs(rank - ((index + x) // 8)) == 3)}

            if p_memory[index] in self.white_pieces:
                own_pieces = self.white_pieces
            else:
                own_pieces = self.black_pieces

            for x in all_knight_moves:
                if p_memory[x] not in own_pieces:
                    legal_moves.append(x)

        return legal_moves

    def find_legal_king_moves(self, p_memory, index, moves):

        legal_moves = []

        black_short = True
        black_long = True
        white_short = True
        white_long = True

        # Check if any castling pieces have been moved
        if any(4 in sublist for sublist in moves):
            black_short = False
            black_long = False
        if any(7 in sublist for sublist in moves):
            black_short = False
        if any(0 in sublist for sublist in moves):
            black_long = False

        if any(60 in sublist for sublist in moves):
            white_short = False
            black_long = False
        if any(63 in sublist for sublist in moves):
            white_short = False
        if any(56 in sublist for sublist in moves):
            white_long = False

        # Check if any castling squares are in view of enemy pieces
        if black_short:
            if self.check_if_king_in_check(p_memory, index, [4, 5, 6]):
                black_short = False
        if black_long:
            if self.check_if_king_in_check(p_memory, index, [1, 2, 3, 4]):
                black_long = False
        if white_short:
            if self.check_if_king_in_check(p_memory, index, [60, 61, 62]):
                white_short = False
        if white_long:
            if self.check_if_king_in_check(p_memory, index, [57, 58, 59, 60]):
                white_long = False

        # white_moves = self.find_all_legal_moves_by_colour('white', p_memory, moves)
        # [print('h..',x) for x in white_moves if x in {60, 61, 62, 63}]

        if black_short and p_memory[5] == 0 and p_memory[5] == 0:
            legal_moves.append(6)
        if black_long and p_memory[3] == 0 and p_memory[2] == 0 and p_memory[1] == 0:
            legal_moves.append(2)

        if white_short and p_memory[61] == 0 and p_memory[62] == 0:
            legal_moves.append(62)
        if white_long and p_memory[59] == 0 and p_memory[58] == 0 and p_memory[57] == 0:
            legal_moves.append(58)

        if p_memory[index] == 2 or p_memory[index] == 8:

            file = index % 8
            rank = index // 8

            directions = {1, 7, 8, 9, -1, -7, -8, -9}
            all_king_moves = {index + x for x in directions if (index + x) in range(64) and (
                    abs(file - ((index + x) % 8)) + abs(rank - ((index + x) // 8))) in {1, 2}}

            if p_memory[index] in self.white_pieces:
                own_pieces = self.white_pieces
            else:
                own_pieces = self.black_pieces

            # Exclusion zone around enemy king
            exclusion_zone = []
            if 2 in own_pieces:
                enemy_king_index = p_memory.index(8)

                enemy_file = enemy_king_index % 8
                enemy_rank = enemy_king_index // 8

                directions = {1, 7, 8, 9, -1, -7, -8, -9}
                all_enemy_king_moves = [enemy_king_index + x for x in directions if
                                        (enemy_king_index + x) in range(64) and (
                                                abs(enemy_file - ((enemy_king_index + x) % 8)) + abs(
                                            enemy_rank - ((enemy_king_index + x) // 8))) in {1, 2}]

                exclusion_zone.extend(all_enemy_king_moves)

            if 8 in own_pieces:
                enemy_king_index = p_memory.index(2)

                enemy_file = enemy_king_index % 8
                enemy_rank = enemy_king_index // 8

                directions = {1, 7, 8, 9, -1, -7, -8, -9}
                all_enemy_king_moves = [enemy_king_index + x for x in directions if
                                        (enemy_king_index + x) in range(64) and (
                                                abs(enemy_file - ((enemy_king_index + x) % 8)) + abs(
                                            enemy_rank - ((enemy_king_index + x) // 8))) in {1, 2}]

                exclusion_zone.extend(all_enemy_king_moves)

            for x in all_king_moves:
                if p_memory[x] not in own_pieces and x not in exclusion_zone:
                    legal_moves.append(x)

        return legal_moves

    def find_legal_queen_moves(self, p_memory, index):

        legal_moves = []

        if p_memory[index] == 1 or p_memory[index] == 7:

            file = index % 8
            rank = index // 8

            all_rook_moves = {x for x in range(64) if x % 8 == file or x // 8 == rank}
            directions_rook = {1, -1, 8, -8}

            if p_memory[index] in self.white_pieces:
                own_pieces = self.white_pieces
                opp_pieces = self.black_pieces
            else:
                own_pieces = self.black_pieces
                opp_pieces = self.white_pieces

            for x in directions_rook:
                square_counter = 1
                while True:
                    test_square_index = index + (x * square_counter)
                    if test_square_index in all_rook_moves:
                        if p_memory[test_square_index] not in own_pieces:
                            legal_moves.append(test_square_index)
                            square_counter += 1
                            if p_memory[test_square_index] in opp_pieces: break
                            continue
                        else:
                            break
                    else:
                        break

            all_bishop_moves = []
            for x in range(64):
                if x % 9 == index % 9 and x % 8 > file and x // 8 > rank:
                    all_bishop_moves.append(x)
                if x % 7 == index % 7 and x % 8 < file and x // 8 > rank:
                    all_bishop_moves.append(x)
                if x % -9 == index % -9 and x % 8 < file and x // 8 < rank:
                    all_bishop_moves.append(x)
                if x % -7 == index % -7 and x % 8 > file and x // 8 < rank:
                    all_bishop_moves.append(x)

            directions_bishop = {9, -9, 7, -7}

            for x in directions_bishop:
                square_counter = 1
                while True:
                    test_square_index = index + (x * square_counter)
                    if test_square_index in all_bishop_moves:
                        if p_memory[test_square_index] not in own_pieces:
                            legal_moves.append(test_square_index)
                            square_counter += 1
                            if p_memory[test_square_index] in opp_pieces: break
                            continue
                        else:
                            break
                    else:
                        break

        return legal_moves

    def find_legal_pawn_moves(self, p_memory, index, moves):

        legal_moves = []

        double_moves = {8, 9, 10, 11, 12, 13, 14, 15, 48, 49, 50, 51, 52, 53, 54, 55}

        if p_memory[index] == 6 or p_memory[index] == 12:

            file = index % 8
            rank = index // 8

            if p_memory[index] in self.white_pieces:
                opp_pieces = self.black_pieces
                direction = -8
            else:
                opp_pieces = self.white_pieces
                direction = 8

            # En passant
            if len(moves) > 0 and (abs(moves[-1][0] - moves[-1][1])) == 16:
                potential_ep = {moves[-1][1] - 1, moves[-1][1] + 1}
                if index in potential_ep:
                    legal_moves.append(moves[-1][0] + -direction)

            # Double move
            if index + (direction * 2) in range(64):
                if index in double_moves and p_memory[index + direction] == 0 and p_memory[
                    index + (direction * 2)] == 0:
                    legal_moves.append(index + (direction * 2))

            # Normal movement
            if index + direction in range(64):
                if p_memory[index + direction] == 0 and (
                        abs(file - ((index + direction) % 8)) + abs(rank - ((index + direction) // 8))) in {1, 2}:
                    legal_moves.append(index + direction)

            if index + direction + 1 in range(64):
                if p_memory[index + direction + 1] in opp_pieces and (
                        abs(file - ((index + direction + 1) % 8)) + abs(rank - ((index + direction + 1) // 8))) in {1,
                                                                                                                    2}:
                    legal_moves.append(index + direction + 1)

            if index + direction - 1 in range(64):
                if p_memory[index + direction - 1] in opp_pieces and (
                        abs(file - ((index + direction - 1) % 8)) + abs(rank - ((index + direction - 1) // 8))) in {1,
                                                                                                                    2}:
                    legal_moves.append(index + direction - 1)

        return legal_moves

    def check_if_king_in_check(self, p_memory, index, potential_moves):

        illegal_move_list = []

        for move in potential_moves:

            temp_p_memory = p_memory.copy()

            # Make the move
            temp_p_memory[move] = temp_p_memory[index]
            if move != index:
                temp_p_memory[index] = 0

            # Determine the piece color
            if p_memory[index] in self.white_pieces:
                king_value = 2
            else:
                king_value = 8

            king_index = temp_p_memory.index(king_value)

            # Check if king is in check in this new position
            if king_value == 2:

                temp_p_memory[king_index] = 6
                temp_legal_moves = self.find_legal_pawn_moves(temp_p_memory, king_index, [])
                if 12 in {temp_p_memory[x] for x in temp_legal_moves}:
                    illegal_move_list.append(move)

                temp_p_memory[king_index] = 1
                temp_legal_moves = self.find_legal_queen_moves(temp_p_memory, king_index)
                if 7 in {temp_p_memory[x] for x in temp_legal_moves}:
                    illegal_move_list.append(move)

                temp_p_memory[king_index] = 3
                temp_legal_moves = self.find_legal_rook_moves(temp_p_memory, king_index)
                if 9 in {temp_p_memory[x] for x in temp_legal_moves}:
                    illegal_move_list.append(move)

                temp_p_memory[king_index] = 4
                temp_legal_moves = self.find_legal_bishop_moves(temp_p_memory, king_index)
                if 10 in {temp_p_memory[x] for x in temp_legal_moves}:
                    illegal_move_list.append(move)

                temp_p_memory[king_index] = 5
                temp_legal_moves = self.find_legal_knight_moves(temp_p_memory, king_index)
                if 11 in {temp_p_memory[x] for x in temp_legal_moves}:
                    illegal_move_list.append(move)

                # excluded because the king can never take another king
                """                
                temp_p_memory[king_index] = 2
                temp_legal_moves = self.find_legal_king_moves(temp_p_memory, king_index, [])
                if 8 in {temp_p_memory[x] for x in temp_legal_moves}:
                    illegal_move_list.append(move)"""

            if king_value == 8:

                temp_p_memory[king_index] = 12
                temp_legal_moves = self.find_legal_pawn_moves(temp_p_memory, king_index, [])
                if 6 in {temp_p_memory[x] for x in temp_legal_moves}:
                    illegal_move_list.append(move)

                temp_p_memory[king_index] = 7
                temp_legal_moves = self.find_legal_queen_moves(temp_p_memory, king_index)
                if 1 in {temp_p_memory[x] for x in temp_legal_moves}:
                    illegal_move_list.append(move)

                temp_p_memory[king_index] = 9
                temp_legal_moves = self.find_legal_rook_moves(temp_p_memory, king_index)
                if 3 in {temp_p_memory[x] for x in temp_legal_moves}:
                    illegal_move_list.append(move)

                temp_p_memory[king_index] = 10
                temp_legal_moves = self.find_legal_bishop_moves(temp_p_memory, king_index)
                if 4 in {temp_p_memory[x] for x in temp_legal_moves}:
                    illegal_move_list.append(move)

                temp_p_memory[king_index] = 11
                temp_legal_moves = self.find_legal_knight_moves(temp_p_memory, king_index)
                if 5 in {temp_p_memory[x] for x in temp_legal_moves}:
                    illegal_move_list.append(move)

                # excluded because the king can never take another king
                """temp_p_memory[king_index] = 8
                temp_legal_moves = self.find_legal_king_moves(temp_p_memory, king_index, [])
                if 2 in {temp_p_memory[x] for x in temp_legal_moves}:
                    illegal_move_list.append(move)"""

        return illegal_move_list

    def find_legal_moves(self, p_memory, index, moves):

        potential_moves = []

        if p_memory[index] == 3 or p_memory[index] == 9:
            potential_moves = self.find_legal_rook_moves(p_memory, index)

        if p_memory[index] == 4 or p_memory[index] == 10:
            potential_moves = self.find_legal_bishop_moves(p_memory, index)

        if p_memory[index] == 5 or p_memory[index] == 11:
            potential_moves = self.find_legal_knight_moves(p_memory, index)

        if p_memory[index] == 2 or p_memory[index] == 8:
            potential_moves = self.find_legal_king_moves(p_memory, index, moves)

        if p_memory[index] == 1 or p_memory[index] == 7:
            potential_moves = self.find_legal_queen_moves(p_memory, index)

        if p_memory[index] == 6 or p_memory[index] == 12:
            potential_moves = self.find_legal_pawn_moves(p_memory, index, moves)

        illegal_moves = self.check_if_king_in_check(p_memory, index, potential_moves)

        legal_moves = [x for x in potential_moves if x not in illegal_moves]

        return legal_moves

    def find_all_legal_moves_by_colour(self, colour, p_memory, moves):
        legal_moves = []

        if colour == "white":
            for idx, x in enumerate(p_memory):
                if x in self.white_pieces:
                    legal_moves.append((idx, self.find_legal_moves(p_memory, idx, moves)))

        if colour == "black":
            for idx, x in enumerate(p_memory):
                if x in self.black_pieces:
                    legal_moves.append((idx, self.find_legal_moves(p_memory, idx, moves)))

        # Remove results that show no move available
        legal_moves = [x for x in legal_moves if x[1]]

        return legal_moves

# tester
# pm = [9, 11, 10, 7, 8, 10, 11, 9, 12, 12, 12, 0, 12, 12, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 12, 6, 6, 6, 3, 5, 4, 1, 2, 4, 5, 3]

# tester = LegalMoves()
# print('Legal Moves:',tester.find_legal_moves(pm, 60, []))

# print('king in check:::', tester.check_if_king_in_check(pm, 60, [60,61,62,63]))
