"""
我们可以为工厂类再创建一个简单工厂，也就是工厂的工厂，用来创建工厂类对象
RuleConfigParserFactoryMap 类是创建工厂对象的工厂类，
getParserFactory() 返回的是缓存好的单例工厂对象。

"""
from singleton import singleton


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
        parser_factory: IRuleConfigParserFactory = RuleConfigParserFactoryMap.instance(
        ).get_parser_factory(rule_config_file_extension)
        if parser_factory is None:
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


# //因为工厂类只包含方法，不包含成员变量，完全可以复用，
# //不需要每次都创建新的工厂类对象，所以，简单工厂模式的第二种实现思路更加合适。
@singleton.Singleton
class RuleConfigParserFactoryMap:
    # //工厂的工厂
    def __init__(self):
        self.__cachedFactories = dict()
        self.__cachedParsers["json"] = JsonRuleConfigParserFactory()
        self.__cachedParsers["xml"] = XmlRuleConfigParserFactory()
        self.__cachedParsers["yaml"] = YamlRuleConfigParserFactory()
        self.__cachedParsers["properties"] = PropertiesRuleConfigParserFactory()

    def get_parser_factory(self, _type: str):
        if _type is None or _type == "":
            return None
        parse_factory = self.__cachedFactories.get(_type.lower())
        return parse_factory


if __name__ == '__main__':
    r1 = RuleConfigParserFactoryMap.instance()
    r2 = RuleConfigParserFactoryMap.instance()
    assert id(r1) == id(r2)
