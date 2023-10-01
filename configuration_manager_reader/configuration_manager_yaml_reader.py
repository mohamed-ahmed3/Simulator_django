from .configuration_manager_abstract import ConfigurationManager
import yaml


class YamlConfigurationManager(ConfigurationManager):
    """
    Concrete class to implement the abstract class when it is yaml file

    methods:
        read
    """

    def read(self):
        """
        read yaml file

        return:
            data
        """
        with open(self.source) as f:
            data = yaml.safe_load(f)

        return data
