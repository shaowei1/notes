"""
为了让类的职责更加单一、代码更加清晰，
我们还可以进一步将 createParser() 函数剥离到一个独立的类中，
让这个类只负责对象的创建。

1. 工厂类中创建对象的方法一般都是 create 开头

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
        parser: IRuleConfigParser = RuleConfigParserFactory.create_parser(
            rule_config_file_extension)
        if parser is None:
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


class RuleConfigParserFactory:
    @staticmethod
    def create_parser(config_format):
        parser: IRuleConfigParser = None
        if config_format == "json":
            parser = JsonRuleConfigParser()
        elif config_format == "xml":
            parser = XmlRuleConfigParser()
        elif config_format == "yaml":
            parser = YamlRuleConfigParser()
        elif config_format == "properties":
            parser = PropertiesRuleConfigParser()
        return parser
