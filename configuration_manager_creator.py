from configuration_manager_reader import configuration_manager_yaml_reader, configuration_manager_json_reader, configuration_manager_database_reader


class ConfigurationManagerCreator:
    def __init__(self, source: str, simulator_name):
        """
        Initializes the configuration manager instance.

        Parameters:
            source: The source of the data. Can be yaml file or json file
        """
        self.source = source
        self.simulator_name = simulator_name

    @classmethod
    def create(cls, source: str, simulator_name):
        """
        Creates an instance from the chosen source.

        Parameters:
            source: The source of the data. Can be yaml file or json file

        """
        if source.endswith('.yml'):
            return configuration_manager_yaml_reader.YamlConfigurationManager(source)

        elif source.endswith('.json'):
            return configuration_manager_json_reader.JsonConfigurationManager(source)

        else:
            return configuration_manager_database_reader.DatabaseReader(source, simulator_name)









