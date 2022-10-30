import pygame
import os
from game.legal_moves import LegalMoves


class Game:

    def __init__(self):

        # Set the game dimensions
        self.width = 800
        self.height = 800
        self.square_size = int(self.width / 8)
        self.all_squares = []

        # Piece colours
        self.black_pieces = {7, 8, 9, 10, 11, 12}
        self.white_pieces = {1, 2, 3, 4, 5, 6}

        # Initialize the game
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.width, self.height))

        # Colours
        self.BLACK = (0, 0, 0)
        self.GREEN = (119, 151, 90)
        self.WHITE = (238, 239, 211)
        self.YELLOW = (232, 226, 39)
        self.BLUE = (38, 203, 209)

        # Create object to find legal moves
        self.lm = LegalMoves()

        # Create object to make engine moves
        self.engine_active = False
        #self.engine = Engine('black')

        # Track current colours turn
        self.whites_turn = True

        # Set up the piece images
        self.images_dict = self.load_images_to_dictionary('C://Users//Conor//PycharmProjects//ChessEngine//resources')

        # Starting FEN
        fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

        # Store the memory of the board
        self.p_memory = self.generate_memory_from_fen(fen)

        self.clicked = None
        self.held = None

        # Store the moves
        self.moves = []

        self.update_window()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():

                # Quit event
                if event.type == pygame.QUIT:
                    running = False

                # Left click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.button == 1:
                        for idx, rect in enumerate(self.all_squares):
                            if rect[0].collidepoint(x, y):

                                if idx == self.clicked:
                                    self.clicked = None
                                elif self.p_memory[idx] == 0:
                                    pass
                                else:
                                    self.clicked = idx
                                    self.held = [idx, x, y]

                # Release left click event
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if self.clicked is not None:
                        for idx, rect in enumerate(self.all_squares):
                            if rect[0].collidepoint(x, y):

                                if idx in self.lm.find_legal_moves(self.p_memory, self.clicked, self.moves):
                                    self.move_piece(self.clicked, idx)
                                    # Update turn colour
                                    if self.p_memory[idx] in self.white_pieces:
                                        self.whites_turn = False
                                    elif self.p_memory[idx] in self.black_pieces:
                                        self.whites_turn = True
                                    self.clicked = None
                                else:
                                    self.held = None
                        self.held = None

                # Update the location of the held piece
                if self.held is not None:
                    x, y = pygame.mouse.get_pos()
                    self.held[1] = x
                    self.held[2] = y

            self.update_after_special_moves()

            # Engine make move
            if self.engine_active:
                if self.engine.engine_colour == 'black' and self.whites_turn is False:
                    if len(self.moves) < 10:
                        engine_move = self.engine.make_a_random_move(self.p_memory, self.moves)
                        print(engine_move)
                    else:
                        engine_move = self.engine.make_a_move(self.p_memory, self.moves)

                    self.move_piece(engine_move[0], engine_move[1])
                    self.whites_turn = True


            # View error board
            #self.p_memory = [9, 11, 10, 7, 8, 10, 11, 9, 12, 12, 12, 12, 12, 12, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 3, 5, 4, 1, 2, 4, 5, 3]

            # Update the on screen graphics
            self.update_window()

        print('pmemory:', self.p_memory)
        print('moves:', self.moves)
        pygame.quit()

    def draw_board(self):
        color = (self.WHITE, self.GREEN)
        self.all_squares = []

        counter = 0
        for file in range(8):
            for rank in range(8):
                color_flip = (file + rank) % 2
                square = (rank * self.square_size, file * self.square_size, self.square_size, self.square_size)

                pygame.draw.rect(self.window, color[color_flip], square)
                self.all_squares.append((pygame.Rect(square), color[color_flip]))

                counter += 1

        if self.clicked is not None:
            c_file = self.clicked % 8
            c_rank = self.clicked // 8
            c_square = (c_file * self.square_size, c_rank * self.square_size, self.square_size, self.square_size)
            pygame.draw.rect(self.window, self.YELLOW, c_square)

        # Show legal moves
        if self.clicked is not None:
            clicked_legal_moves = self.lm.find_legal_moves(self.p_memory, self.clicked, self.moves)
            for x in clicked_legal_moves:
                cl_file = x % 8
                cl_rank = x // 8
                cl_square = (cl_file * self.square_size, cl_rank * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(self.window, self.BLUE, cl_square)

    def draw_pieces_from_memory(self):
        for idx, piece in enumerate(self.p_memory):
            file = idx % 8
            rank = idx // 8

            if piece == 0:
                pass
            else:
                self.window.blit(self.images_dict[piece], (file * self.square_size, rank * self.square_size))

    def draw_held_piece(self):
        if self.held is not None:
            h_file = self.held[0] % 8
            h_rank = self.held[0] // 8
            h_square = (h_file * self.square_size, h_rank * self.square_size, self.square_size, self.square_size)
            pygame.draw.rect(self.window, self.YELLOW, h_square)

            held_piece = self.p_memory[self.held[0]]
            held_location = ((self.held[1] - (self.square_size / 2)), (self.held[2]) - (self.square_size / 2))
            self.window.blit(self.images_dict[held_piece], held_location)

    def update_window(self):
        # Fill the entire window with black to clear the screen
        self.window.fill(self.BLACK)

        # Draw the board with empty squares
        self.draw_board()

        # Draw the pieces on the board
        self.draw_pieces_from_memory()

        # Draw held piece
        self.draw_held_piece()

        # Update the window and tick the game-clock
        pygame.display.flip()
        self.clock.tick(60)

    def load_images_to_dictionary(self, path_to_directory):
        image_dict = {}

        for filename in os.listdir(path_to_directory):
            if filename.endswith('.png'):
                path = os.path.join(path_to_directory, filename)
                key = int(filename[:-4])
                image_dict[key] = pygame.image.load(path)

        for img in image_dict:
            image_dict[img] = pygame.transform.smoothscale(image_dict[img], (self.square_size, self.square_size))

        return image_dict

    def move_piece(self, start, end):

        self.p_memory[end] = self.p_memory[start]
        self.p_memory[start] = 0

        self.moves.append((start, end))

    def update_after_special_moves(self):
        if len(self.moves) > 0:
            # Castling
            if self.moves[-1] == (60, 62):
                self.p_memory[61], self.p_memory[63] = self.p_memory[63], self.p_memory[61]
                self.moves.append((63, 61))
            elif self.moves[-1] == (60, 58):
                self.p_memory[56], self.p_memory[59] = self.p_memory[59], self.p_memory[56]
                self.moves.append((56, 59))
            elif self.moves[-1] == (4, 6):
                self.p_memory[7], self.p_memory[5] = self.p_memory[5], self.p_memory[7]
                self.moves.append((7, 5))
            elif self.moves[-1] == (4, 2):
                self.p_memory[0], self.p_memory[3] = self.p_memory[3], self.p_memory[0]
                self.moves.append((0, 3))

            # En passant
            if len(self.moves) > 1:
                if self.p_memory[self.moves[-2][1]] in {6, 12} and abs(self.moves[-2][0] - self.moves[-2][1]) == 16:
                    if self.p_memory[self.moves[-2][1]] in self.white_pieces:
                        jumped = self.moves[-2][0] - 8
                    else:
                        jumped = self.moves[-2][0] + 8
                    if self.p_memory[self.moves[-1][1]] in {6, 12} and abs(self.moves[-1][0] - self.moves[-1][1]) in {7,
                                                                                                                      9,
                                                                                                                      -7,
                                                                                                                      -9}:
                        if jumped == self.moves[-1][1]:
                            self.p_memory[self.moves[-2][1]] = 0

            # Upgrading pawns
            if self.moves[-1][1] in range(0, 8) or self.moves[-1][1] in range(56, 64):
                # check if white moved to back and give options
                if self.p_memory[self.moves[-1][1]] == 6:
                    self.p_memory[self.moves[-1][1]] = 1
                # check if black moved to back and give options
                if self.p_memory[self.moves[-1][1]] == 12:
                    self.p_memory[self.moves[-1][1]] = 7

    @staticmethod
    def generate_memory_from_fen(fen):
        fen_dict = {'Q': 1, 'K': 2, 'R': 3, 'B': 4, 'N': 5, 'P': 6, 'q': 7, 'k': 8, 'r': 9, 'b': 10, 'n': 11, 'p': 12}
        p_memory = []
        for x in fen:
            if x in fen_dict:
                p_memory.append(fen_dict[x])
            elif x.isdigit():
                [p_memory.append(0) for y in range(int(x))]
            elif x == '/':
                continue
            else:
                break
        return p_memory
