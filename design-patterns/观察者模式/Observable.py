"""
邮件订阅、RSS Feeds

attach
detach

设计模式要干的事情就是解耦。
创建型模式是将创建和使用代码解耦，
结构型模式是将不同功能代码解耦，
行为型模式是将不同的行为代码解耦，
具体到观察者模式，它是将观察者和被观察者代码解耦

如果大数据征信系统提供了发送用户注册信息的 RPC 接口，
我们仍然可以沿用之前的实现思路，在 handleRegSuccess() 函数中调用 RPC 接口来发送数据。
但是，我们还有更加优雅、更加常用的一种实现方式，
那就是基于消息队列（Message Queue，比如 ActiveMQ）来实现。

发布-订阅模型
生产-消费模型
"""
from abc import abstractmethod

import typing


class Observer:
    @abstractmethod
    def update(self, message):
        pass


class Subject:
    @abstractmethod
    def register_observer(self, observer: Observer):
        pass

    @abstractmethod
    def remove_observer(self, observer: Observer):
        pass

    @abstractmethod
    def notify_observer(self, message):
        pass


class ConcreteSubject(Subject):
    def __init__(self):
        self.observers: typing.List[Observer] = []

    def register_observer(self, observer: Observer):
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        self.observers.remove(observer)

    def notify_observer(self, message):
        for observer in self.observers:
            observer.update(message)


class ConcreteObserverOne(Observer):
    def update(self, message):
        print(f'ConcreteObserverOne: {message}')


class ConcreteObserverTwo(Observer):
    def update(self, message):
        print(f'ConcreteObserverTwo: {message}')


if __name__ == '__main__':
    subject = ConcreteSubject()
    subject.register_observer(ConcreteObserverOne())
    subject.register_observer(ConcreteObserverTwo())
    subject.notify_observer('new message')
