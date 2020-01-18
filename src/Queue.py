class Queue:
    def __init__(self, *args):
        #__queue means the value is private
        self.__queue = []
        for value in args:
            self.__queue.append(value)

    def enqueue(self, value):
        self.__queue.append(value)

    def dequeue(self):
        return self.__queue.pop(0)

    def peek(self):
        return self.__queue[0]

    def is_empty(self):
        if(len(self.__queue) > 0):
            return False
        return True

    def size(self):
        return len(self.__queue)
