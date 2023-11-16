import os
import json
import datetime


class LocalDataBank:
    def __init__(self, config):
        self._path = os.path.abspath(config["path"])
        if not os.path.isdir(self._path):
            os.makedirs(self._path)
        print("Create local data bank @ " + str(self._path))
        info_file = os.path.join(self._path, "db_info.json")
        if os.path.isfile(info_file):
            with open(info_file, "r") as f:
                self._info = json.load(f)
        else:
            self._info = {
                "table_files": {},
                "created_on": datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S"),
            }
        self._tables = {}
        for name, table_file in self._info["table_files"].items():
            if os.path.isfile(table_file):
                with open(table_file, "r") as f:
                    self._tables[name] = json.load(f)

    def __str__(self):
        return "Local({}), {} tables".format(self._path, len(self._tables))

    def add_table(self, table_name):
        if table_name not in self._info["table_files"]:
            self._info["table_files"][table_name] = os.path.join(
                self._path, table_name + ".json"
            )
        if table_name not in self._tables:
            self._tables[table_name] = {}
        return self._tables[table_name]

    def drop_table(self, table_name):
        if table_name in self._info["table_files"]:
            if os.path.isfile(self._info["table_files"][table_name]):
                os.remove(self._info["table_files"][table_name])
            self._info["table_files"].pop(table_name)

    def get_table(self, table_name):
        return self._tables.get(table_name, {})

    def add_item(self, table_name, key, info):
        table = self.add_table(table_name)
        if key in table:
            table[key].update(info)
        else:
            info["id"] = len(table)
            if "datetime" not in info:
                info["datetime"] = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
            table[key] = info

    def get_item(self, table_name, key):
        assert table_name in self._tables, "Can not find {} from tables".format(
            table_name
        )
        return self._tables[table_name].get(key)

    def commit(self):
        with open(os.path.join(self._path, "db_info.json"), "w") as f:
            f.write(json.dumps(self._info, indent=2))
        for name, content in self._tables.items():
            with open(self._info["table_files"][name], "w") as f:
                f.write(json.dumps(content, indent=2))
