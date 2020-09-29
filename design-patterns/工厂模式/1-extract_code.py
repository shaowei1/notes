"""
为了让代码逻辑更加清晰，可读性更好，我们要善于将功能独立的代码块封装成函数。
按照这个设计思路，我们可以将代码中涉及 parser 创建的部分逻辑剥离出来，抽象成 createParser() 函数
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
        parser: IRuleConfigParser = self.__create_parser(
            rule_config_file_extension)
        if parser is None:
            raise InvalidRuleConfigException(
                f"Rule config file format is not supported: {rule_config_filepath}"
            )

        config_text = ""
        # 从ruleConfigFilePath文件中读取配置文本到configText中
        rule_config: RuleConfig = parser.parse(config_text)
        return rule_config

    def __create_parser(self, config_format):
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

    def __get_file_extension(self, filepath):
        # ...解析文件名获取扩展名，比如rule.json，返回json
        return "json"
