"""
Factory Design Pattern

工厂方法和抽象工厂

我们根据配置文件的后缀（json、xml、yaml、properties），
选择不同的解析器（JsonRuleConfigParser、XmlRuleConfigParser……），
将存储在文件中的配置解析成内存对象 RuleConfig。

"""


class IRuleConfigParser:
    pass


class JsonRuleConfigParser(IRuleConfigParser):
    pass


class XmlRuleConfigParser(IRuleConfigParser):
    pass


class YamlRuleConfigParser(IRuleConfigParser):
    pass


class PropertiesRuleConfigParser(IRuleConfigParser):
    pass


class InvalidRuleConfigException(Exception):
    pass


class RuleConfig:
    pass


class RuleConfigSource:
    def load(self, rule_config_filepath):
        rule_config_file_extension = self.__get_file_extension(
            rule_config_filepath)
        parser: IRuleConfigParser = None
        if rule_config_file_extension == "json":
            parser = JsonRuleConfigParser()
        elif rule_config_file_extension == "xml":
            parser = XmlRuleConfigParser()
        elif rule_config_file_extension == "yaml":
            parser = YamlRuleConfigParser()
        elif rule_config_file_extension == "properties":
            parser = PropertiesRuleConfigParser()
        else:
            raise InvalidRuleConfigException(
                f"Rule config file format is not supported: {rule_config_filepath}"
            )

        config_text = ""
        # 从ruleConfigFilePath文件中读取配置文本到configText中
        rule_config: RuleConfig = parser.parse(config_text)
        return rule_config

    def __get_file_extension(self, filepath):
        # ...解析文件名获取扩展名，比如rule.json，返回json
        return "json"
