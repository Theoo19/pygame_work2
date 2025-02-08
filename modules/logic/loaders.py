from pygame import image as _image
from pygame.mixer import Sound as _Sound
from typing import Sequence as _Sequence


class _File:
    """A class to represent a file with a path and its loaded content."""

    def __init__(self, path, content):
        """Initiate _File object.

        :param path: path to file
        :type path: str
        :param content: opened content of file
        :type content: object
        """
        self.path = path
        self.content = content


class _VariableLoader:
    """A class to represent a dictionary to store variables in."""

    def __init__(self):
        """Initiate _VariableLoader object."""
        self._loaded = dict()

    def load(self, name, value):
        """Load variable.

        :param name: key, name of the variable
        :type name: str
        :param value: value of variable to save
        :type value: object
        """
        self._loaded[name] = value

    def get(self, name):
        """Get variable.

        :param name: key, name of the variable
        :type name: str
        :return: value of variable to get
        :rtype: object
        """
        return self._loaded[name]

    def __setitem__(self, key, value):
        """x[key] = value

        :param key: key, name of the variable
        :type key: str
        :param value: value of variable to save
        :type value: object
        :return:
        :rtype:
        """
        return self.load(key, value)

    def __getitem__(self, item):
        """x[key]

        :param item: key, name of the variable
        :type item: str
        :return: value of variable to get
        :rtype: object
        """
        return self.get(item)


class _FileLoader(_VariableLoader):
    """A class to represent a dictionary to store files in."""

    def load(self, name, path):
        """Load file.

        :param name: key, name of the file
        :type name: str
        :param path: path to file to open
        :type path: str
        """
        self._loaded[name] = _File(path, open(path, 'rb'))

    def get(self, name):
        """Get file.

        :param name: key, name of the file
        :type name: str
        :return: content of file to get
        :rtype: object
        """
        return self._loaded[name].content


class _ImageLoader(_FileLoader):
    """A class to represent a dictionary to store images in."""

    def load(self, name, path):
        """Load image.

        :param name: key, name of the image
        :type name: str
        :param path: path to image to open
        :type path: str
        """
        self._loaded[name] = _File(path, _image.load(path).convert_alpha())


class _SoundLoader(_FileLoader):
    """A class to represent a dictionary to store sounds in."""

    def load(self, name, path):
        """Load sound.

        :param name: key, name of the sound
        :type name: str
        :param path: path to sound to open
        :type path: str
        """
        self._loaded[name] = _File(path, _Sound(path))


class FunctionLoader:
    """A class to represent a container for a function reference and its needed parameters."""

    def __init__(self, *args):
        """Initiate FunctionLoader object.

        function: reference to function to execute, or None
        parameters: tuple of needed parameters for possible function to execute

        :param args: args[0] -> object, args[1:] parameters, if len(args) = 0 -> None
        """
        if len(args) > 0:
            self.function = args[0]
        else:
            self.function = None
        self.parameters = args[1:]

    def set_parameters(self, *parameters):
        """Set parameters to certain values.

        :param parameters: needed parameters for the function.
        """
        self.parameters = parameters

    def execute(self):
        """Execute function."""
        if self.function is not None:
            return self.function(*self.parameters)

    @staticmethod
    def from_variable(obj):
        """Create FunctionLoader with properties depending on the variable.

        :param obj: any
        :type obj: FunctionLoader or _Sequence or function or None
        :rtype: FunctionLoader
        """
        if type(obj) is FunctionLoader:
            return obj
        if isinstance(obj, _Sequence) and not isinstance(obj, (str, bytes, bytearray)):
            return FunctionLoader(*obj)
        if callable(obj):
            return FunctionLoader(obj)
        if obj is None:
            return FunctionLoader()
        print("Warning: type: {} is not valid. Loading default FunctionLoader.".format(type(obj)))
        return FunctionLoader()


Variables = _VariableLoader()
Fonts = _VariableLoader()
Images = _ImageLoader()
Sounds = _SoundLoader()
