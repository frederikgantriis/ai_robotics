class Queue[T]:
    def __init__(self):
        self.queue = []

    def enqueue(self, item: T):
        self.queue.append(item)

    def dequeue(self) -> T:
        if not self.is_empty():
            return self.queue.pop(0)
        raise IndexError()

    def peek(self) -> T:
        if not self.is_empty():
            return self.queue[0]
        raise IndexError()

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def size(self) -> int:
        return len(self.queue)

    def __repr__(self) -> str:
        return str(self.queue)
