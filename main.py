import tkinter as tk
import random

# Crear la ventana del juego
window = tk.Tk()
window.title("Snake Game")

# Dimensiones de la cuadrícula
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20

# Tamaño de los cuadros de la cuadrícula
GRID_CELL_SIZE = 20

# Direcciones de movimiento
DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0)
}


class SnakeGame:

    # Actualizar la pantalla
    def __init__(self, window):
        self.window = window
        self.window.title("Snake Game")

        # Crear la cuadrícula del juego
        self.canvas = tk.Canvas(window, width=GRID_WIDTH * GRID_CELL_SIZE, height=GRID_HEIGHT * GRID_CELL_SIZE, bg="black")
        self.canvas.pack()

        # Inicializar la serpiente
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice(list(DIRECTIONS.values()))

        # Inicializar la comida
        self.food = self.generate_food()

        # Puntuación
        self.score = 0

        # Dibujar la serpiente y la comida
        self.draw_snake()
        self.draw_food()

        # Configurar los eventos de teclado
        self.window.bind("<Key>", self.on_key_press)

        # Iniciar el bucle del juego
        self.update()

    def draw_snake(self):
        self.canvas.delete("snake")

        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, (x + 1) * GRID_CELL_SIZE, (y + 1) * GRID_CELL_SIZE, fill="green", tags="snake")

    def draw_food(self):
        self.canvas.delete("food")

        x, y = self.food
        self.canvas.create_oval(x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, (x + 1) * GRID_CELL_SIZE, (y + 1) * GRID_CELL_SIZE, fill="red", tags="food")

    def generate_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            if (x, y) not in self.snake:
                return x, y

    def move_snake(self):
        head = self.snake[0]
        dx, dy = self.direction
        new_head = (head[0] + dx, head[1] + dy)

        # Comprobar si la serpiente ha chocado consigo misma o con los bordes de la cuadrícula
        if (
            new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT
        ):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # Comprobar si la serpiente ha comido la comida
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
            self.draw_food()
        else:
            self.snake.pop()

        self.draw_snake()

    def game_over(self):
        self.canvas.create_text(GRID_WIDTH * GRID_CELL_SIZE // 2, GRID_HEIGHT * GRID_CELL_SIZE // 2, text=("Game Over, tu puntuación ha sido: " + str(self.score)), fill="white", font=("Arial", 20), tags="game_over")

    def on_key_press(self, event):
        key = event.keysym

        if key in DIRECTIONS:
            new_direction = DIRECTIONS[key]

            # Comprobar que la serpiente no se mueva en la dirección opuesta
            if (
                self.direction[0] + new_direction[0] != 0 or
                self.direction[1] + new_direction[1] != 0
            ):
                self.direction = new_direction

    def update(self):
        self.move_snake()

        if "game_over" not in self.canvas.gettags("game_over"):
            self.window.after(200, self.update)


# Iniciar el juego
game = SnakeGame(window)

# Ejecutar el bucle principal de la interfaz gráfica
window.mainloop()
