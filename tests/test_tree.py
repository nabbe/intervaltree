from unittest import TestCase

from interval_tree import Tree


class C:
    def __init__(self, value, top, left, bottom, right):
        self.__box = (top, bottom), (left, right)
        self.__value = value

    @property
    def box(self):
        return self.__box

    @property
    def value(self):
        return self.__value


class TestIntervalTree2D(TestCase):
    def test_roundtrip(self):
        testee = Tree(
            [(0, 300), (0, 300)],
            key=lambda v: v.box
        )
        #                              top  left  bottom  right
        testee.add(C('up-left',         10,   10,    100,   100))
        testee.add(C('up-right',        10,  170,    100,   280))
        testee.add(C('bottom-left',    170,   10,    280,   100))
        testee.add(C('bottom-right',   170,  170,    280,   280))
        testee.add(C('up-center',       10,   10,    100,   280))
        testee.add(C('center-left',     10,   10,    280,   100))
        testee.add(C('center-right',    10,  170,    280,   280))
        testee.add(C('bottom-center',  170,   10,    280,   280))
        testee.add(C('center-center',  140,  140,    170,   170))

        for point, expected in [
            (
                (11, 11),
                ['up-left', 'center-left', 'up-center']
            ),
            (
                (11, 279),
                ['up-right', 'center-right', 'up-center'], 
            ),
            (
                (279, 11),
                ['bottom-left', 'bottom-center', 'center-left'],
            ),
            (
                (279, 279),
                ['bottom-right', 'bottom-center', 'center-right']
            ),
            (
                (150, 150),
                ['center-center']
            ),
            (
                (3, 5),
                []
            )
        ]:
            with self.subTest(i=point):
                actual = [c.value for c in testee.query(point)]
                actual.sort()
                expected = list(sorted(expected))
                self.assertEqual(actual, expected)

    def test_it_is_iterable(self):
        testee = Tree(
            [(0, 300), (0, 300)],
            key=lambda v: v.box
        )
        #                              top  left  bottom  right
        testee.add(C('up-left',          0,    0,    149,  149))
        testee.add(C('bottom-left',    150,    0,    299,  149))
        testee.add(C('up-right',         0,  150,    149,  299))
        testee.add(C('bottom-right',   150,  150,    299,  299))

        expected = ['up-left', 'up-right', 'bottom-left', 'bottom-right']
        expected.sort()

        actual = [node.value for node in testee]
        actual.sort()

        self.assertEqual(expected, actual)

    def test_on_edge(self):
        testee = Tree(
            [(0, 300), (0, 300)],
            key=lambda v: v.box
        )
        #                              top  left  bottom  right
        testee.add(C('up-left',          0,    0,    149,  149))
        testee.add(C('bottom-left',    150,    0,    299,  149))
        testee.add(C('up-right',         0,  150,    149,  299))
        testee.add(C('bottom-right',   150,  150,    299,  299))

        for point, expected in [
            ((  0,   0), ['up-left']),
            ((  1,   1), ['up-left']),
            ((149, 149), ['up-left']),
            ((148, 148), ['up-left']),
            ((  0, 149), ['up-left']),
            ((  1, 148), ['up-left']),
            ((149,   0), ['up-left']),
            ((148,   1), ['up-left']),

            ((  0, 150), ['up-right']),
            ((  1, 151), ['up-right']),
            ((149, 299), ['up-right']),
            ((148, 298), ['up-right']),
            ((  0, 299), ['up-right']),
            ((  1, 298), ['up-right']),
            ((149, 150), ['up-right']),
            ((148, 151), ['up-right']),

            ((150,   0), ['bottom-left']),
            ((151,   1), ['bottom-left']),
            ((299, 149), ['bottom-left']),
            ((298, 148), ['bottom-left']),
            ((150, 149), ['bottom-left']),
            ((151, 148), ['bottom-left']),
            ((299,   0), ['bottom-left']),
            ((298,   1), ['bottom-left']),

            ((150, 150), ['bottom-right']),
            ((151, 151), ['bottom-right']),
            ((299, 299), ['bottom-right']),
            ((298, 298), ['bottom-right']),
            ((150, 299), ['bottom-right']),
            ((151, 298), ['bottom-right']),
            ((299, 150), ['bottom-right']),
            ((298, 151), ['bottom-right']),
        ]:
            with self.subTest(i=point):
                actual = [c.value for c in testee.query(point)]
                actual.sort()
                expected = list(sorted(expected))
                self.assertEqual(actual, expected)

