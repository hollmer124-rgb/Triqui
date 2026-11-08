import tkinter as tk
import pygame
import random
import sys

# ==========================================
# CONSTANTES DE DISEÑO (Estilo Kick / Neón)
# ==========================================
BG_BLACK = (0, 0, 0)           # Negro profundo para el fondo
NEON_GREEN = (57, 255, 20)     # Verde fosforescente brillante
NEON_HEX = "#39FF14"           # Código Hex para Tkinter
FONT_NAME = "Impact"           # Fuente gruesa y urbana

# ==========================================
# CLASE 1: VENTANA DE BIENVENIDA (TKINTER)
# ==========================================
class WelcomeWindow:
    """
    Clase encargada de manejar la interfaz gráfica inicial usando Tkinter.
    Captura los nombres de los jugadores y da inicio al juego.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TRIQUI - NEON EDITION")
        self.root.geometry("450x500")
        self.root.configure(bg="black")
        self.root.resizable(True,True)
        
        # Variables para almacenar la decisión y nombres
        self.start_game = False
        self.p1_name = "Jugador 1"
        self.p2_name = "Jugador 2"

        self._build_ui()

    def _build_ui(self):
        """Construye todos los elementos visuales de la ventana Tkinter"""
        # Título principal
        title = tk.Label(self.root, text="THE BEST TRIQUI", font=(FONT_NAME, 36), bg="black", fg=NEON_HEX)
        title.pack(pady=30)

        # Contenedor para Jugador 1
        frame_p1 = tk.Frame(self.root, bg="black")
        frame_p1.pack(pady=15)
        lbl_p1 = tk.Label(frame_p1, text="JUGADOR 1 (X):", font=(FONT_NAME, 16), bg="black", fg=NEON_HEX)
        lbl_p1.pack()
        self.entry_p1 = tk.Entry(frame_p1, font=(FONT_NAME, 14), bg="black", fg=NEON_HEX, 
                                 insertbackground=NEON_HEX, relief="solid", highlightbackground=NEON_HEX, highlightthickness=2)
        self.entry_p1.insert(0, "Jugador 1") # Valor por defecto
        self.entry_p1.pack(pady=5)

        # Contenedor para Jugador 2
        frame_p2 = tk.Frame(self.root, bg="black")
        frame_p2.pack(pady=15)
        lbl_p2 = tk.Label(frame_p2, text="JUGADOR 2 (O):", font=(FONT_NAME, 16), bg="black", fg=NEON_HEX)
        lbl_p2.pack()
        self.entry_p2 = tk.Entry(frame_p2, font=(FONT_NAME, 14), bg="black", fg=NEON_HEX, 
                                 insertbackground=NEON_HEX, relief="solid", highlightbackground=NEON_HEX, highlightthickness=2)
        self.entry_p2.insert(0, "Jugador 2") # Valor por defecto
        self.entry_p2.pack(pady=5)

        # Botón START
        btn_start = tk.Button(self.root, text="START", font=(FONT_NAME, 20), bg=NEON_HEX, fg="black",
                              relief="solid", bd=3,
                              command=self._on_start)
        btn_start.pack(pady=40, ipadx=30, ipady=5)

    def _on_start(self):
        """Se ejecuta al presionar Start. Guarda nombres y cierra Tkinter."""
        self.p1_name = self.entry_p1.get().strip() or "Jugador 1"
        self.p2_name = self.entry_p2.get().strip() or "Jugador 2"
        self.start_game = True
        self.root.destroy() # Cierra la ventana de bienvenida

    def run(self):
        """Inicia el loop principal de Tkinter y retorna los datos al cerrar."""
        self.root.mainloop()
        return self.p1_name, self.p2_name, self.start_game


# ==========================================
# CLASE 2: MOTOR DEL JUEGO (PYGAME)
# ==========================================
class TriquiGame:
    """
    Clase que maneja la lógica, gráficos y eventos del juego en Pygame.
    """
    def __init__(self, p1_name, p2_name, scores):
        pygame.init()
        # Configuraciones de ventana
        self.width = 600
        self.height = 700 # 100px extra para el marcador superior
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The Best Triqui")

        # Estado del juego
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.scores = scores # Lista [score_p1, score_p2]
        self.board = [[None for _ in range(3)] for _ in range(3)] # Matriz 3x3
        
        # Turno aleatorio (0 = P1/X, 1 = P2/O)
        self.current_turn = random.choice([0, 1])
        self.state = "PLAYING" # "PLAYING", "GAMEOVER"
        self.winner = None

        # Fuentes gruesas (Impact)
        self.font_score = pygame.font.SysFont(FONT_NAME, 30)
        self.font_big = pygame.font.SysFont(FONT_NAME, 80)
        self.font_btn = pygame.font.SysFont(FONT_NAME, 35)

        # Definición de zonas clicables para los botones de fin de juego
        self.btn_rects = {
            "PLAY_AGAIN": pygame.Rect(100, 300, 400, 60),
            "HOME": pygame.Rect(100, 390, 400, 60),
            "EXIT": pygame.Rect(100, 480, 400, 60)
        }

    def draw_top_bar(self):
        """Dibuja el contenedor superior con nombres y marcador"""
        # Separador inferior del marcador
        pygame.draw.line(self.screen, NEON_GREEN, (0, 100), (self.width, 100), 5)
        
        # Texto Jugador 1 (Izquierda) - Resalta si es su turno
        color_p1 = NEON_GREEN if self.current_turn == 0 and self.state == "PLAYING" else (100, 100, 100)
        p1_text = self.font_score.render(f"{self.p1_name} (X)", True, color_p1)
        self.screen.blit(p1_text, (20, 35))

        # Marcador (Centro)
        score_text = self.font_score.render(f"{self.scores[0]} : {self.scores[1]}", True, NEON_GREEN)
        score_rect = score_text.get_rect(center=(self.width // 2, 50))
        self.screen.blit(score_text, score_rect)

        # Texto Jugador 2 (Derecha) - Resalta si es su turno
        color_p2 = NEON_GREEN if self.current_turn == 1 and self.state == "PLAYING" else (100, 100, 100)
        p2_text = self.font_score.render(f"(O) {self.p2_name}", True, color_p2)
        self.screen.blit(p2_text, (self.width - p2_text.get_width() - 20, 35))

    def draw_grid(self):
        """Dibuja la cuadrícula 3x3 estilo neón"""
        # Líneas verticales
        pygame.draw.line(self.screen, NEON_GREEN, (200, 100), (200, 700), 5)
        pygame.draw.line(self.screen, NEON_GREEN, (400, 100), (400, 700), 5)
        # Líneas horizontales
        pygame.draw.line(self.screen, NEON_GREEN, (0, 300), (600, 300), 5)
        pygame.draw.line(self.screen, NEON_GREEN, (0, 500), (600, 500), 5)

    def draw_figures(self):
        """Dibuja las X y las O en el tablero basándose en la matriz"""
        for row in range(3):
            for col in range(3):
                # Centro de la celda
                x_center = col * 200 + 100
                y_center = row * 200 + 100 + 100 # +100 por el marcador
                
                if self.board[row][col] == 'X':
                    # Dibuja X (Dos líneas cruzadas gruesas)
                    pygame.draw.line(self.screen, NEON_GREEN, (x_center - 50, y_center - 50), (x_center + 50, y_center + 50), 15)
                    pygame.draw.line(self.screen, NEON_GREEN, (x_center + 50, y_center - 50), (x_center - 50, y_center + 50), 15)
                elif self.board[row][col] == 'O':
                    # Dibuja O (Un círculo grueso)
                    pygame.draw.circle(self.screen, NEON_GREEN, (x_center, y_center), 60, 15)

    def draw_game_over(self):
        """Pinta la pantalla de negro y muestra las opciones de fin de ronda"""
        self.screen.fill(BG_BLACK)
        
        # Anuncio del ganador
        if self.winner == 'X':
            msg = f"¡GANÓ {self.p1_name.upper()}!"
        elif self.winner == 'O':
            msg = f"¡GANÓ {self.p2_name.upper()}!"
        else:
            msg = "¡EMPATE!"
            
        title = self.font_big.render(msg, True, NEON_GREEN)
        title_rect = title.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title, title_rect)

        # Dibujar Botones
        labels = {"PLAY_AGAIN": "VOLVER A JUGAR", "HOME": "VOLVER AL INICIO", "EXIT": "SALIR"}
        
        for key, rect in self.btn_rects.items():
            # Obtener posición del mouse para efecto hover (brillo)
            mouse_pos = pygame.mouse.get_pos()
            color = NEON_GREEN if rect.collidepoint(mouse_pos) else (50, 150, 50)
            
            # Dibujar borde del botón
            pygame.draw.rect(self.screen, color, rect, 5)
            # Dibujar texto del botón
            txt_surf = self.font_btn.render(labels[key], True, color)
            txt_rect = txt_surf.get_rect(center=rect.center)
            self.screen.blit(txt_surf, txt_rect)

    def check_win(self):
        """Verifica si alguien alineó 3 figuras o si hay empate"""
        # Chequeo de filas, columnas y diagonales
        for i in range(3):
            # Filas
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] is not None:
                return self.board[i][0]
            # Columnas
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] is not None:
                return self.board[0][i]
                
        # Diagonales
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return self.board[0][2]

        # Chequeo de empate (tablero lleno sin ganador)
        is_full = all(cell is not None for row in self.board for cell in row)
        if is_full:
            return "TIE"
            
        return None # El juego continúa

    def handle_click(self, pos):
        """Procesa el clic dependiendo de si estamos jugando o en menú de fin"""
        if self.state == "PLAYING":
            x, y = pos
            if y < 100: return # Clic en el marcador, ignorar

            # Calcular fila y columna clickeada (0, 1 o 2)
            col = x // 200
            row = (y - 100) // 200

            # Si la celda está vacía, colocar figura
            if self.board[row][col] is None:
                # Turno 0 es P1 (X), Turno 1 es P2 (O)
                figure = 'X' if self.current_turn == 0 else 'O'
                self.board[row][col] = figure
                
                # Verificar victoria después del movimiento
                result = self.check_win()
                if result:
                    self.winner = result
                    self.state = "GAMEOVER"
                    # Aumentar marcador
                    if result == 'X': self.scores[0] += 1
                    elif result == 'O': self.scores[1] += 1
                else:
                    # Cambiar turno si nadie ganó
                    self.current_turn = 1 - self.current_turn

        elif self.state == "GAMEOVER":
            # Verificar si se hizo clic en algún botón
            for action, rect in self.btn_rects.items():
                if rect.collidepoint(pos):
                    return action # Retorna "PLAY_AGAIN", "HOME" o "EXIT"
        return None

    def run(self):
        """Loop principal de Pygame (60 FPS)"""
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    action = self.handle_click(pygame.mouse.get_pos())
                    if action: # Si el handle_click retornó una acción del menú final
                        pygame.quit()
                        return action

            # Renderizado Gráfico
            if self.state == "PLAYING":
                self.screen.fill(BG_BLACK)
                self.draw_top_bar()
                self.draw_grid()
                self.draw_figures()
            elif self.state == "GAMEOVER":
                self.draw_game_over()

            pygame.display.update()
            clock.tick(60)

# ==========================================
# CLASE 3: CONTROLADOR PRINCIPAL
# ==========================================
class GameController:
    """
    Gestiona el flujo entre la ventana de Tkinter y el entorno de Pygame.
    """
    def __init__(self):
        self.scores = [0, 0]

    def start(self):
        """Punto de entrada de la aplicación"""
        while True:
            # 1. Iniciar ventana de bienvenida (Tkinter)
            welcome = WelcomeWindow()
            p1, p2, start_flag = welcome.run()

            # Si el usuario cerró la ventana sin presionar Start, salir del programa
            if not start_flag:
                break

            # 2. Iniciar bucle de partidas en Pygame
            while True:
                # Instanciamos el juego pasándole nombres y el marcador actual
                game = TriquiGame(p1, p2, self.scores)
                action = game.run() # Pygame toma control hasta que se acabe la ronda

                # Evaluación de la decisión final de la ronda
                if action == "PLAY_AGAIN":
                    self.scores = game.scores # Mantiene el puntaje y repite el bucle interno
                    continue 
                elif action == "HOME":
                    self.scores = [0, 0] # Resetea puntajes
                    break # Rompe bucle interno, vuelve a iniciar el while exterior (Tkinter)
                elif action == "EXIT":
                    sys.exit() # Cierra el programa por completo

if __name__ == "__main__":
    app = GameController()
    app.start()