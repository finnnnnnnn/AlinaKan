import random
import typing as tp
from copy import deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            pygame.display.flip()
            clock.tick(self.speed)
            self.grid = self.get_next_generation()
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        a = []
        for i in range(self.cell_height):
            b = []
            for j in range(self.cell_width):
                if randomize:
                    b.append(random.choice((0, 1)))
                else:
                    b.append(0)
            a.append(b)
        return a

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j]:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size),
                    )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        x, y = cell
        a = []
        if x == 0 and y == 0:  # левый верхний угол
            a.extend([self.grid[x + 1][y], self.grid[x][y + 1], self.grid[x + 1][y + 1]])
        elif x == 0 and y == self.cell_width - 1:  # правый верхний угол
            a.extend([self.grid[x][y - 1], self.grid[x + 1][y], self.grid[x + 1][y - 1]])
        elif x == 0 and y != self.cell_width - 1 and y != 0:  # верхняя строка
            a.extend(
                [
                    self.grid[x][y - 1],
                    self.grid[x + 1][y],
                    self.grid[x][y + 1],
                    self.grid[x + 1][y + 1],
                    self.grid[x + 1][y - 1],
                ]
            )
        elif x == self.cell_height - 1 and y == 0:  # левый нижний угол
            a.extend([self.grid[x - 1][y], self.grid[x][y + 1], self.grid[x - 1][y + 1]])
        elif x == self.cell_height - 1 and y == self.cell_width - 1:  # правый нижний угол
            a.extend([self.grid[x][y - 1], self.grid[x - 1][y], self.grid[x - 1][y - 1]])
        elif x == self.cell_height - 1 and y != 0 and y != self.cell_width - 1:  # нижняя строка
            a.extend(
                [
                    self.grid[x - 1][y],
                    self.grid[x - 1][y - 1],
                    self.grid[x - 1][y + 1],
                    self.grid[x][y - 1],
                    self.grid[x][y + 1],
                ]
            )
        elif y == 0 and x != 0 and x != self.cell_height - 1:  # левый стоблик
            a.extend(
                [
                    self.grid[x + 1][y],
                    self.grid[x - 1][y],
                    self.grid[x][y + 1],
                    self.grid[x - 1][y + 1],
                    self.grid[x + 1][y + 1],
                ]
            )
        elif y == self.cell_width - 1 and x != 0 and x != self.cell_height - 1:  # правый столбк
            a.extend(
                [
                    self.grid[x][y - 1],
                    self.grid[x - 1][y],
                    self.grid[x + 1][y],
                    self.grid[x - 1][y - 1],
                    self.grid[x + 1][y - 1],
                ]
            )
        else:
            a.extend(
                [
                    self.grid[x + 1][y],
                    self.grid[x - 1][y],
                    self.grid[x][y + 1],
                    self.grid[x][y - 1],
                    self.grid[x - 1][y + 1],
                    self.grid[x - 1][y - 1],
                    self.grid[x + 1][y + 1],
                    self.grid[x + 1][y - 1],
                ]
            )
        return a

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        res = deepcopy(self.grid)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                neighbours = sum(self.get_neighbours((i, j)))
                if (neighbours != 2 and neighbours != 3) and self.grid[i][j] == 1:
                    res[i][j] = 0
                elif neighbours == 3 and self.grid[i][j] == 0:
                    res[i][j] = 1
        return res
