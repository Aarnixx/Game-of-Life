import sys
import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor

TILE_SIZE = 5
ROWS, COLS = 100, 100
STARTER_TILES = 1500


class GameOfLifeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(COLS * TILE_SIZE, ROWS * TILE_SIZE)
        self.tile_dictionary = {}

        self.generate_grid()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_grid)
        self.timer.start(100)

    def generate_grid(self):
        for i in range(ROWS):
            for j in range(COLS):
                self.tile_dictionary[(i, j)] = "white"
        for _ in range(STARTER_TILES):
            pos = random.choice(list(self.tile_dictionary.keys()))
            self.tile_dictionary[pos] = "black"

    def set_glider(self, top_left=(1, 1)):
        i, j = top_left
        pattern = [
            (0, 1),
            (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]
        for di, dj in pattern:
            if 0 <= i + di < ROWS and 0 <= j + dj < COLS:
                self.tile_dictionary[(i + di, j + dj)] = "black"

    def count_live_neighbors(self, pos):
        i, j = pos
        neighbors = [
            (i-1, j-1), (i-1, j), (i-1, j+1),
            (i, j-1),           (i, j+1),
            (i+1, j-1), (i+1, j), (i+1, j+1)
        ]
        count = 0
        for ni, nj in neighbors:
            if 0 <= ni < ROWS and 0 <= nj < COLS:
                if self.tile_dictionary.get((ni, nj)) == "black":
                    count += 1
        return count

    def update_grid(self):
        new_tile_dictionary = {}

        for pos in self.tile_dictionary:
            live_neighbors = self.count_live_neighbors(pos)
            if self.tile_dictionary[pos] == "black":
                if live_neighbors in [2, 3]:
                    new_tile_dictionary[pos] = "black"
                else:
                    new_tile_dictionary[pos] = "white"
            else:
                if live_neighbors == 3:
                    new_tile_dictionary[pos] = "black"
                else:
                    new_tile_dictionary[pos] = "white"

        self.tile_dictionary = new_tile_dictionary
        self.update()  # uudeleen maalaus

        alive_count = sum(1 for c in self.tile_dictionary.values() if c == "black")
        #print(f"Alive cells: {alive_count}")
        if alive_count == 0:
            pass
            #print("All cells died.")

    def paintEvent(self, event):
        painter = QPainter(self)
        for (i, j), color in self.tile_dictionary.items():
            if color == "black":
                painter.setBrush(QColor(0, 0, 0))
            else:
                painter.setBrush(QColor(255, 255, 255))
            painter.setPen(QColor(255, 255, 255)) # Valkoiset
            x = j * TILE_SIZE
            y = i * TILE_SIZE
            painter.drawRect(x, y, TILE_SIZE, TILE_SIZE)


def main():
    app = QApplication(sys.argv)
    window = GameOfLifeWidget()
    window.setWindowTitle("Game of Life")
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
