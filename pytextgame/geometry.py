# -- coding: utf-8 --
'''geometry necessary to address the grid of characters on the screen'''

import math


class Position(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def in_direction(self, dir):
        '''Create a new position vector as the sum of
        this and another
        '''
        return Position(self.x + dir.dx, self.y + dir.dy)

    def translate(self, dir):
        '''translate in the mathematical sense means to move
        one vector in the direction of another vector
        '''
        self.x += dir.dx
        self.y += dir.dy

    def position(self):
        '''Return a new position vector that matches this one'''
        return Position(self.x, self.y)

    def direction(self):
        '''Return a direction vector built from this position vector'''
        return Direction(self.x, self.y)

    def direction_to(self, other):
        '''Create a direction vector from another position to this one'''
        return Direction(other.x - self.x, other.y - self.y)

    def distance(self, other):
        '''find the Euclidian distance between this vector and another'''
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self):
        return 'Position(%d, %d)' % (self.x, self.y)


class Rectangle(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def area(self):
        '''Return the area of the rectangle'''
        return self.width * self.height

    def diagonal(self):
        '''Return a positionless vector parallel
        to the diagonal of this rectangle
        '''
        return Direction(self.width, self.height)

    def __repr__(self):
        return 'Rectangle(%d, %d, %d, %d)' % (self.x, self.y, self.width, self.height)


class Direction(object):

    def __init__(self, dx, dy, name=None):
        self.dx = dx
        self.dy = dy
        self.name = name

    def invert(self):
        '''flip the direction of this vector'''
        self.dx *= -1
        self.dy *= -1

    def scale(self, factor):
        '''increase the length of this vector'''
        self.dx *= factor
        self.dy *= factor

    def descale(self, divisor):
        '''decrease the length of this vector'''
        self.dx /= divisor
        self.dy /= divisor

    def __str__(self):
        if self.name is None:
            return 'd(%d, %d)' % (self.dx, self.dy)

        return self.name
