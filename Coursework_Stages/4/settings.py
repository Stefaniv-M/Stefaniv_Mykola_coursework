import copy


class WrongSettingValue(BaseException):
    """
    Error for a case when value of an exception is being set
    to one that is not in possible values.
    """
    pass


class Setting:
    """
    Class representing a setting.
    """
    def __init__(self, setting_name, possible_values, current_value, description, possible_values_str=None):
        """
        Initialise Setting by its string name, possible values, current value, description. possible_values
        can be list or function. If possible_values is list and can fit in short space (subjectively),
        possible_values_str can remain None. Otherwise possible_values_str are string representation of all possible
        values which is able to explain them and fit on screen. If possible_values is a function and
        possible_values_str remains None, ValueError will be raised.
        Description is a description of a setting.
        possible_values can be list of str or function.
        :param setting_name: str
        :param possible_values: list of str or function
        :param current_value: str
        :param possible_values_str: NoneType or str
        """
        # Checking if input is correct:
        if not isinstance(setting_name, str):
            raise ValueError("Name of a setting must be string.")
        elif not isinstance(current_value, str):
            raise ValueError("Current value of a setting must be str.")
        elif not isinstance(description, str):
            raise ValueError("Description of a setting must be str.")

        # Getting possible values:
        possible_values_func, possible_values_str = self._set_possible_values(possible_values, possible_values_str)

        # Saving all values:
        self._setting_name = setting_name
        self._possible_values_func = possible_values_func
        self._possible_values_str = possible_values_str

        # Setting current value:
        if self._possible_values_func(current_value):
            self._current_value = current_value
        else:
            raise ValueError("Current value not in possible values!")

        # Setting description:
        self._description = description

    def get_setting_name(self):
        """
        Return string name of the setting.
        :return: str
        """
        return self._setting_name

    def get_current_value(self):
        """
        Return current value of the setting.
        :return: str
        """
        return self._current_value

    def get_description(self):
        """
        Return description of a current setting.
        :return: str
        """
        return self._description

    def __str__(self):
        """
        Return string representation of a Setting. It looks
        like this:
        some_setting = "On" ["On, "Off", "Unknown"]
        :return: str
        """
        return '{} = "{}" {}\n{}'.format(self._setting_name,
                                         self._current_value,
                                         self._possible_values_str,
                                         self.get_description())

    def __repr__(self):
        """
        Return string information about the setting so that it
        can be written into a text file to save it. Only name
        of the setting and current value are recorded - files are
        for modifying settings, not creating them. Example:
        some_setting = On

        (no parentheses)
        :return: str
        """
        return "{} = {}".format(self._setting_name,
                                self._current_value)

    @staticmethod
    def _set_possible_values(possible_values, possible_values_str):
        """
        Return tuple with two elements: function func_1(a), which returns True if a is in possible_values, and
        with string representation of possible values.
        :param possible_values: func or list
        :param possible_values_str: str or NoneType
        :return: tuple
        """
        # If possible_values are not list and possible_values_str is None:
        if (not isinstance(possible_values, list)) and possible_values_str is None:
            raise ValueError("If possible_values is not a list, possible_values_str must not be None.")

        # If possible_values is a list:
        if isinstance(possible_values, list):
            def result_func(elem):
                return elem in possible_values

            # If string representation of list is absent, create one:
            if possible_values_str is None:
                result_str = str(possible_values)
            else:
                result_str = possible_values_str

        # If possible_values is a function:
        elif callable(possible_values):
            def result_func(elem):
                return possible_values(elem)

            result_str = possible_values_str

        # Otherwise raise an error:
        else:
            raise ValueError("possible_values must be list or function.")

        return tuple([result_func, result_str])

    def set_value(self, current_value):
        """
        Change current value of setting or return ValueError.
        :param current_value: str
        :return: NoneType
        """
        # Checking:
        if not self._possible_values_func(current_value):
            raise ValueError("Setting value not in possible_values.")

        # Setting:
        self._current_value = current_value


class Settings:
    """
    Class representing a group of settings.
    """
    def __init__(self, list_of_settings):
        """
        Initialise by list of settings.
        :param list_of_settings: list
        """
        # Checking argument (it must be a list that
        # contains only Setting objects):
        if not isinstance(list_of_settings, list) or \
            False in [isinstance(elem, Setting) for elem
                      in list_of_settings]:
            raise ValueError("Instance of a Settings class "
                             "can be only initialised by list of"
                             " Setting objects.")

        # Initialising:
        self._all_settings = []

        for setting in list_of_settings:
            self._all_settings.append(setting)

    def setting_by_name(self, setting_name):
        """
        Return Setting object for modifying it.
        :param setting_name: str
        :return: Setting
        """
        # Checking input:
        if not isinstance(setting_name, str):
            raise ValueError("Name of the setting must be str.")

        # Checking if there is a setting:
        if setting_name not in [setting.get_setting_name()
                                for setting in
                                self._all_settings]:
            raise ValueError("There is no such setting.")

        # If everything is ok:
        return self._all_settings[[setting.get_setting_name()
                                   for setting in
                                   self._all_settings
                                   ].index(setting_name)]

    def read_file(self, file_name):
        """
        Read information from the file with settings and
        change current settings. Ignore lines with errors.
        :param file_name: str
        :return: NoneType
        """
        def read_line(file_line):
            """
            Try to change value of Setting described in line of
            the file. Argument is a line. If something is
            incorrect, error will be raised.
            :param file_line: str
            :return: NoneType
            """
            # First input check:
            if not isinstance(file_line, str):
                raise ValueError("Line of the file must be str.")

            # List of words from line of a file (and removing "\n" from the end of the line):
            words = file_line[:-1].split(" ")

            # Second input check (if third word exists and if second word is "="):
            if words[1] != "=" or len(words[2]) == 0:
                raise ValueError("Line of the setting file is "
                                 "not correct:\n" + file_line)

            # Trying to change a setting (if arguments are
            # incorrect, errors will be raised):
            setting = self.setting_by_name(words[0])
            setting.set_value(words[2])

        # Opening a file and getting list of lines:
        file = open(file_name, "r")
        lines = file.readlines()
        file.close()

        # Working about each line (ignore corrupted lines):
        for line in lines:
            try:
                read_line(line)
            # Yes, cause is broad, but I want to ignore all
            # errors:
            except:
                pass

    def write_into_file(self, file_name):
        """
        Write settings into a text file (or rewrite it).
        :param file_name: str
        :return: NoneType
        """
        # Checking argument:
        if not isinstance(file_name, str):
            raise ValueError("File name must be str.")

        # Opening the file for writing:
        file = open(file_name, "w")

        # Writing:
        for setting in self._all_settings:
            file.write(repr(setting) + "\n")

        # Closing a file:
        file.close()

    def __str__(self):
        """
        Return string representation of all the settings of a group.
        :return: str
        """
        result_str = ""
        for setting in self._all_settings:
            result_str = result_str + "\n" + str(setting) + "\n"
        # [1:] to remove "\n" which is in the beginning of a result_str:
        return result_str[1:]
