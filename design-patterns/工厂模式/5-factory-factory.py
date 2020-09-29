"""
我们可以为工厂类再创建一个简单工厂，也就是工厂的工厂，用来创建工厂类对象
RuleConfigParserFactoryMap 类是创建工厂对象的工厂类，
getParserFactory() 返回的是缓存好的单例工厂对象。

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


class IRuleConfigParserFactory:
    def create_parser(self):
        pass


class JsonRuleConfigParserFactory(IRuleConfigParserFactory):
    def create_parser(self):
        return JsonRuleConfigParser()


class XmlRuleConfigParserFactory(IRuleConfigParserFactory):
    def create_parser(self):
        return XmlRuleConfigParser()


class YamlRuleConfigParserFactory(IRuleConfigParserFactory):
    def create_parser(self):
        return YamlRuleConfigParser()


class PropertiesRuleConfigParserFactory(IRuleConfigParserFactory):
    def create_parser(self):
        return PropertiesRuleConfigParser()


class InvalidRuleConfigException(Exception):
    pass


class RuleConfig:
    pass


class RuleConfigSource:
    def load(self, rule_config_filepath):
        rule_config_file_extension = self.__get_file_extension(
            rule_config_filepath)
        parser_factory: IRuleConfigParserFactory = None
        if rule_config_file_extension == "json":
            parser_factory = JsonRuleConfigParserFactory()
        elif rule_config_file_extension == "xml":
            parser_factory = XmlRuleConfigParserFactory()
        elif rule_config_file_extension == "yaml":
            parser_factory = YamlRuleConfigParserFactory()
        elif rule_config_file_extension == "properties":
            parser_factory = PropertiesRuleConfigParserFactory()
        else:
            raise InvalidRuleConfigException(
                f"Rule config file format is not supported: {rule_config_filepath}"
            )

        parser = parser_factory.create_parser()
        config_text = ""
        # 从ruleConfigFilePath文件中读取配置文本到configText中
        rule_config: RuleConfig = parser.parse(config_text)
        return rule_config

    def __get_file_extension(self, filepath):
        # ...解析文件名获取扩展名，比如rule.json，返回json
        return "json"
