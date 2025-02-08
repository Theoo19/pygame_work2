
class TimeLine:
    def __init__(self, *events):
        self.__events = list(*events)  # Currently TimeLine will only support CountDown objects

    def update(self):
        for event in self.__events:
            event.tick()
        self.__events = list(event for event in self.__events if event.get_active())
    
    def append(self, event):
        self.__events.append(event)
        event.start()

    def clear(self):
        self.__events.clear()

    def count(self, event):
        self.__events.count(event)

    def extend(self, events):
        self.extend(events)
        for event in events:
            event.start()

    def index(self, event, start=0, stop=0):
        self.__events.index(event, start, stop)

    def insert(self, index, event):
        self.__events.insert(index, event)
        event.start()

    def pop(self, index):
        self.__events.pop(index)

    def remove(self, event):
        self.__events.remove(event)

    def reverse(self):
        self.__events.reverse()

    def __getitem__(self, item):
        return self.__events[item]

    def __iter__(self):
        self.__index = 0
        return self

    def __len__(self):
        return len(self.__events)

    def __next__(self):
        if self.__index < len(self.__events):
            shape = self.__events[self.__index]
            self.__index += 1
            return shape
        else:
            raise StopIteration
