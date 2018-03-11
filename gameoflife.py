"""conway's game of life
"""
from PySide.QtGui import QGridLayout, QWidget, QPushButton
from PySide.QtGui import QApplication, QVBoxLayout, QColor
from PySide.QtCore import QTimer


INTERVAL = 100
INDEX_ALIVE = 2


class GameOfLifeWidget(QWidget):
    """game of life widget with grid and tools
    """
    def _handle_timeout(self):
        grid = _play(self.grid)
        del self.grid
        self.grid = grid
        self._update_gui()

    def _update_gui(self):
        for y_pos in range(self.height):
            for x_pos in range(self.width):
                _, _, life = self.grid[y_pos][x_pos]
                neighbours = _get_neighbours_of_cell(self.grid, self.grid[y_pos][x_pos])
                lifes = [
                    list(n)[INDEX_ALIVE] for n in neighbours
                    if list(n)[INDEX_ALIVE]
                ]
                total_lifes = len(lifes)
                weight = ((float(total_lifes) / 8.0) * 175.0) + 80.0

                if life:
                    color = QColor(weight, weight / 2, weight / 2)
                    self.buttons[y_pos][x_pos].setStyleSheet(
                        """QWidget { background-color: %s; }""" % color.name())
                else:

                    color = QColor(1, 1, weight)
                    self.buttons[y_pos][x_pos].setStyleSheet(
                        """QWidget { background-color: %s; }""" % color.name())
                    # self.buttons[y][x].setStyleSheet(None)

    def _handle_click(self):
        for y_pos, row in enumerate(self.buttons):
            for x_pos, button in enumerate(row):
                if button == self.sender():
                    _, _, life = self.grid[y_pos][x_pos]
                    new_life = not life
                    self.grid[y_pos][x_pos] = (x_pos, y_pos, new_life)
        self._update_gui()

    def __init__(self, width, height, grid):
        super(GameOfLifeWidget, self).__init__()
        self.setWindowTitle('Game Of Life')
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        main_layout = QVBoxLayout()
        self.buttons = []
        self.grid = grid
        self.width = width
        self.height = height
        self.timer = QTimer()
        self.timer.setInterval(INTERVAL)
        self.timer.timeout.connect(self._handle_timeout)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self._handle_start)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self._handle_clear)

        main_layout.addLayout(layout)
        main_layout.addWidget(self.start_button)
        main_layout.addWidget(self.clear_button)
        self.setLayout(main_layout)
        for y_pos in range(height):
            row = []
            self.buttons.append(row)
            for x_pos in range(width):
                button = QPushButton()
                row.append(button)
                button.setMaximumWidth(20)
                button.setMaximumHeight(20)
                button.clicked.connect(self._handle_click)
                layout.addWidget(button, y_pos, x_pos)
        self._update_gui()

    def _handle_clear(self):
        grid = _make_grid_from_size(self.width, self.height)
        del self.grid
        self.grid = grid
        self._update_gui()

    def _handle_start(self):
        if self.timer.isActive():
            self.start_button.setText('Start')
            self.timer.stop()
        else:
            self.start_button.setText('Stop')
            self.timer.start()


def _get_neighbours_of_cell(grid, cell):
    """return neighbour cells
    """
    x_pos, y_pos, _ = cell
    if x_pos + 1 < len(grid[y_pos]):
        right = x_pos + 1
    else:
        right = 0

    if x_pos - 1 >= 0:
        left = x_pos - 1
    else:
        left = -1

    if y_pos - 1 >= 0:
        top = y_pos - 1
    else:
        top = -1

    if y_pos + 1 < len(grid):
        bottom = y_pos + 1
    else:
        bottom = 0

    yield grid[y_pos][right]
    yield grid[y_pos][left]
    yield grid[top][x_pos]
    yield grid[bottom][x_pos]
    yield grid[top][left]
    yield grid[top][right]
    yield grid[bottom][right]
    yield grid[bottom][left]


def _make_grid_from_data(data):
    rows = []
    for i, row_i in enumerate(data):
        row = []
        rows.append(row)
        for j, life in enumerate(row_i):
            row.append((
                i,
                j,
                life,
            ))

    return rows


def _make_grid_from_size(width, height):
    grid = []
    for i in range(height):
        row = []
        grid.append(row)
        for j in range(width):
            row.append((
                j,
                i,
                False,
            ))
    return grid


def _format_grid(grid):
    text = ''
    for row in grid:
        for cell in row:
            if cell[INDEX_ALIVE]:
                text += '1'
            else:
                text += '0'
        text += '\n'
    return text


def _play(grid):
    new_grid = []
    for row in grid:
        new_row = []
        new_grid.append(new_row)
        for cell in row:
            x_pos, y_pos, alive = cell
            neighbours = list(_get_neighbours_of_cell(grid, cell))
            health_neighbours = [list(n)[INDEX_ALIVE] for n in neighbours]
            health_neighbours = [life_i for life_i in health_neighbours if life_i]

            if alive and len(health_neighbours) < 2:
                new_life = False
            elif alive and (len(health_neighbours) == 2 or len(health_neighbours) == 3):
                new_life = True
            elif alive and len(health_neighbours) > 3:
                new_life = False
            elif not alive and len(health_neighbours) == 3:
                new_life = True
            else:
                new_life = False
            new_row.append((
                x_pos,
                y_pos,
                new_life,
            ))
    return new_grid


def main():
    """start the game of life in a new widget
    """
    width, height = 20, 20
    grid = _make_grid_from_size(width, height)

    app = QApplication([])
    game_of_life_widget = GameOfLifeWidget(width, height, grid)
    game_of_life_widget.show()
    app.exec_()


if __name__ == '__main__':
    main()
