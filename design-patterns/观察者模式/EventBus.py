"""
事件总线

 Google Guava EventBus
异步非阻塞观察者模式

 其中一种是：在每个 handleRegSuccess() 函数中创建一个新的线程执行代码逻辑；
    频繁地创建和销毁线程比较耗时，并且并发线程数无法控制，创建过多的线程会导致堆栈溢出

 另一种是：在 UserController 的 register() 函数中使用线程池来执行每个观察者的 handleRegSuccess() 函数。
    线程池、异步执行逻辑都耦合在了 register() 函数中，增加了这部分业务代码的维护成本。

框架:
    框架的作用有：隐藏实现细节，降低开发难度，做到代码复用，解耦业务与非业务代码，让程序员聚焦业务开发
"""
import time
import uuid
import typing
from inspect import isfunction
import concurrent.futures


class ObserverRegistry:
    registry = dict()

    def register(self, obj):
        observer_actions: typing.Dict[
            object, typing.List[ObserverAction]] = self.findAllObserverActions(obj)
        for key, values in observer_actions.items():
            if values:
                self.registry[key] = values

    def getMatchedObserverActions(self, event):
        matched_observers = set()
        posted_event_types = event.registry.registry.keys()
        for eventType, eventActions in self.registry.items():
            for posted_event_type in posted_event_types:
                if issubclass(posted_event_type, eventType):
                    matched_observers.update(eventActions)
        return matched_observers

    def findAllObserverActions(self, obj):
        observer_actions = {obj: self.getAnnotatedMethods(obj)}
        return observer_actions

    def getAnnotatedMethods(self, obj):
        annotatedMethods = []
        for method in vars(obj).values():
            if isfunction(method) and hasattr(method, 'subscribe') and method.subscribe is True:
                annotatedMethods.append(ObserverAction(obj, method))
        return annotatedMethods


class directExecutor:
    def submit(self, func, *args, **kwargs):
        return func(*args, **kwargs)


class EventBus:
    executor = None
    registry = ObserverRegistry()

    def __init__(self, executor=None):

        if executor is not None:
            self.executor = executor
        else:
            self.executor = directExecutor()

    def register(self, obj: object):
        """注册观察者
        必须接受实现了同一 Observer 接口的类对象
        """
        self.registry.register(obj)

    def unregister(self, obj: object):
        """从 EventBus 中删除某个观察者"""
        pass

    def post(self, event):
        """用来给观察者发送消息"""
        observer_actions: typing.Set[ObserverAction] = self.registry.getMatchedObserverActions(
            self)
        for observer_action in observer_actions:
            self.executor.submit(observer_action.execute, event)


def subscribe(func, *args, **kwargs):
    """表示 @subscribe 注解的方法"""
    func.subscribe = True
    return func


class AsyncEventBus(EventBus):

    def __init__(self, executor=None):
        super(AsyncEventBus, self).__init__(executor)


class Preconditions:
    @staticmethod
    def checkNotNull(target):
        return bool(target is not None)


class ObserverAction:
    target = None  # 表示观察者类
    method = None  # 表示方法

    def __init__(self, target, method):
        self.target = target
        self.method = method

    def execute(self, event: object):
        """

        :param event: event是method方法的参数
        :return:
        InvocationTargetException | IllegalAccessException
        """
        self.method(self.target, event)


class PromotionService:
    def issueNewUserExperienceCash(self, user_id):
        time.sleep(1)
        print(f"issueNewUserExperienceCash: {user_id}")


class NotificationService:
    def sendInboxMessage(self, user_id, word):
        time.sleep(1)
        print(f"notice: {user_id} ==> {word}")


class UserService:
    def register(self, telephone, password):
        print(f'telephone, password: {telephone, password}')
        return str(uuid.uuid4())


class RegPromotionObserver:
    promotionService = PromotionService()  # 依赖注入

    @subscribe
    def handle_reg_success(self, user_id):
        self.promotionService.issueNewUserExperienceCash(user_id)

    def no_handle(self):
        pass


class RegNotificationObserver:
    notificationService = NotificationService()  # 依赖注入

    @subscribe
    def handle_reg_success(self, user_id):
        self.notificationService.sendInboxMessage(user_id, "Welcome...")


class UserController:
    userService = UserService()  # 依赖注入
    eventBus = AsyncEventBus(executor=concurrent.futures.ThreadPoolExecutor(max_workers=5))
    # eventBus = EventBus()

    #   一次性设置好，之后也不可能动态的修改
    def set_reg_observers(self, observers: typing.List[object]):
        for observer in observers:
            self.eventBus.register(observer)

    def register(self, telephone: str, password: str):
        user_id = self.userService.register(telephone, password)
        self.eventBus.post(user_id)
        return user_id


if __name__ == '__main__':
    user_controller = UserController()
    user_controller.set_reg_observers([RegPromotionObserver, RegNotificationObserver])
    user_controller.register('18342910538', 'cdd2083')
    print('main')
