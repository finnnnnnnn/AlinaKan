import pathlib
import random
import typing as tp
from copy import deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]
curr_generation = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        a = []
        for i in range(self.rows):
            b = []
            for j in range(self.cols):
                if randomize:
                    b.append(random.choice((0, 1)))
                else:
                    b.append(0)
            a.append(b)
        return a

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        x, y = cell
        a = []
        if x == 0 and y == 0:  # левый верхний угол
            a.extend(
                [
                    self.curr_generation[x + 1][y],
                    self.curr_generation[x][y + 1],
                    self.curr_generation[x + 1][y + 1],
                ]
            )
        elif x == 0 and y == self.cols - 1:  # правый верхний угол
            a.extend(
                [
                    self.curr_generation[x][y - 1],
                    self.curr_generation[x + 1][y],
                    self.curr_generation[x + 1][y - 1],
                ]
            )
        elif x == 0 and y != self.cols - 1 and y != 0:  # верхняя строка
            a.extend(
                [
                    self.curr_generation[x][y - 1],
                    self.curr_generation[x + 1][y],
                    self.curr_generation[x][y + 1],
                    self.curr_generation[x + 1][y + 1],
                    self.curr_generation[x + 1][y - 1],
                ]
            )
        elif x == self.rows - 1 and y == 0:  # левый нижний угол
            a.extend(
                [
                    self.curr_generation[x - 1][y],
                    self.curr_generation[x][y + 1],
                    self.curr_generation[x - 1][y + 1],
                ]
            )
        elif x == self.rows - 1 and y == self.cols - 1:  # правый нижний угол
            a.extend(
                [
                    self.curr_generation[x][y - 1],
                    self.curr_generation[x - 1][y],
                    self.curr_generation[x - 1][y - 1],
                ]
            )
        elif x == self.rows - 1 and y != 0 and y != self.cols - 1:  # нижняя строка
            a.extend(
                [
                    self.curr_generation[x - 1][y],
                    self.curr_generation[x - 1][y - 1],
                    self.curr_generation[x - 1][y + 1],
                    self.curr_generation[x][y - 1],
                    self.curr_generation[x][y + 1],
                ]
            )
        elif y == 0 and x != 0 and x != self.rows - 1:  # левый стоблик
            a.extend(
                [
                    self.curr_generation[x + 1][y],
                    self.curr_generation[x - 1][y],
                    self.curr_generation[x][y + 1],
                    self.curr_generation[x - 1][y + 1],
                    self.curr_generation[x + 1][y + 1],
                ]
            )
        elif y == self.cols - 1 and x != 0 and x != self.rows - 1:  # правый столбк
            a.extend(
                [
                    self.curr_generation[x][y - 1],
                    self.curr_generation[x - 1][y],
                    self.curr_generation[x + 1][y],
                    self.curr_generation[x - 1][y - 1],
                    self.curr_generation[x + 1][y - 1],
                ]
            )
        else:
            a.extend(
                [
                    self.curr_generation[x + 1][y],
                    self.curr_generation[x - 1][y],
                    self.curr_generation[x][y + 1],
                    self.curr_generation[x][y - 1],
                    self.curr_generation[x - 1][y + 1],
                    self.curr_generation[x - 1][y - 1],
                    self.curr_generation[x + 1][y + 1],
                    self.curr_generation[x + 1][y - 1],
                ]
            )
        return a

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        res = deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = sum(self.get_neighbours((i, j)))
                if (neighbours != 2 and neighbours != 3) and self.curr_generation[i][j] == 1:
                    res[i][j] = 0
                elif neighbours == 3 and self.curr_generation[i][j] == 0:
                    res[i][j] = 1
        return res

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations == self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "rt", encoding="utf-8") as f:
            data = f.readlines()
        print(data, type(data))
        for i in range(len(data)):
            data[i] = list(map(int, list(data[i].rstrip())))
        game = GameOfLife((len(data[0]), len(data)))
        game.curr_generation = data
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        data = "\n".join(map(lambda x: "".join(map(str, x)), self.curr_generation))
        with open(filename, "wt", encoding="utf-8") as f:
            f.write(data)
