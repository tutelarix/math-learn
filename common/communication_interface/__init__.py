from enum import IntEnum


class CommunicationInterface(IntEnum):
    """
    Represents possible communication interfaces
    """

    Empty = 0
    Console = 1
    GUI = 2
