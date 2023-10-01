import json
from datetime import datetime

from .configuration_manager_abstract import ConfigurationManager


class JsonConfigurationManager(ConfigurationManager):
    def read(self):
        """
        read json file

        return:
            data
        """
        with open(self.source) as f:
            jsondata = f.read()
            data = json.loads(jsondata)

            date_str = data['start_date']
            date_format = '%Y-%m-%d'
            date_obj = datetime.strptime(date_str, date_format)
            data['start_date'] = date_obj

        return data