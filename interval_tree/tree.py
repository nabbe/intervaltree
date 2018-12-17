class Tree:
    """
    Interval Tree.

    It stores N-dimensional rectangles,
    and perform hit-test by a point in N-dimensional space.
    """

    def __init__(self, space, key=None):
        """
        :param key:
            Function to decide a minimum-bounding-box of a entry.
            Each minimum-bounding-box is decided
            with value pairs of (min, max) for each dimension.
            e.g, [(top, bottom), (left, right), (shallow, deep), (past, future), ...]
            Each values should be numeric
            (divide-able with integer, compareable with each other).
            In default or pass None, `Tree` sorts by each entry by itself.
        """
        self.__key = key
        self.__space = space = tuple(space)
        self.__centers = [sum(band) / 2 for band in space]
        self.__items = []
        self.__subtree = {}

    def __indexed(self, item):
        key = item if self.__key is None else self.__key(item)
        return key, item

    def __add(self, box, item):
        bucket = []
        for c, (mini, maxi) in zip(self.__centers, box):
            if mini < c <= maxi:
                self.__items.append((box, item))
                return
            bucket.append(maxi < c)

        bucket = tuple(bucket)
        try:
            self.__subtree[bucket].add(item)
        except KeyError:
            self.__subtree[bucket] = subtree = type(self)(
                (
                    (lowlim, c) if lower else (c, uplim)
                    for c, (lowlim, uplim), lower
                    in zip(self.__centers, self.__space, bucket)
                ),
                key=self.__key,
            )
            subtree.__add(box, item)

    def add(self, item):
        box, item = self.__indexed(item)
        self.__add(box, item)

    def query(self, point):
        """
        Query entries which contains the `point`. except root.
        """
        for box, item in self.__items:
            if all(mini <= v <= maxi for v, (mini, maxi) in zip(point, box)):
                yield item
        bucket = tuple(
            x < c for c, x in zip(self.__centers, point)
        )
        try:
            yield from self.__subtree[bucket].query(point)
        except KeyError:
            return

    def __iter__(self):
        yield from (item for box, item in self.__items)
        for subt in self.__subtree.values():
            yield from subt
        
