"""
如果 parser 可以复用，为了节省内存和对象创建的时间，
我们可以将 parser 事先创建好缓存起来。
当调用 createParser() 函数的时候，我们从缓存中取出 parser 对象直接使用。

"""


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


import typing


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
        parser: IRuleConfigParser = RuleConfigParserFactory().create_parser(
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


@singleton
class RuleConfigParserFactory:
    def __init__(self):
        self.__cachedParsers: typing.Dict[str, IRuleConfigParser] = dict()
        self.__cachedParsers["json"] = JsonRuleConfigParser()
        self.__cachedParsers["xml"] = XmlRuleConfigParser()
        self.__cachedParsers["yaml"] = YamlRuleConfigParser()
        self.__cachedParsers["properties"] = PropertiesRuleConfigParser()

    def create_parser(self, config_format: str):
        if config_format is None or config_format == "":
            return None  # //返回null还是IllegalArgumentException全凭你自己说了算
        parser: IRuleConfigParser = self.__cachedParsers.get(config_format.lower())
        return parser


if __name__ == '__main__':
    cl1 = RuleConfigParserFactory()
    cl2 = RuleConfigParserFactory()
    assert id(cl1) == id(cl2)
