class JsonRuleConfigParser:
    pass


class JsonSystemConfigParser:
    pass


class IConfigParserFactory:
    def createRuleParser(self):
        pass

    def createSystemParser(self):
        pass

    # //此处可以扩展新的parser类型，比如IBizConfigParser


class JsonConfigParserFactory(IConfigParserFactory):
    def createRuleParser(self):
        return JsonRuleConfigParser()

    def createSystemParser(self):
        return JsonSystemConfigParser()
