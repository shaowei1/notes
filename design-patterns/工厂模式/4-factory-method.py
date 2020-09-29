"""
如果我们非得要将 if 分支逻辑去掉，那该怎么办呢？
比较经典处理方法就是利用多态。按照多态的实现思路，对上面的代码进行重构


这样当我们新增一种 parser 的时候，
只需要新增一个实现了 IRuleConfigParserFactory 接口的 Factory 类即可。
工厂类对象的创建逻辑又耦合进了 load() 函数中
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
