from abc import abstractmethod

import typing


class RegObserver:
    @abstractmethod
    def handle_reg_success(self, user_id):
        pass


class PromotionService:
    pass


class NotificationService:
    pass


class UserService:
    pass


class RegPromotionObserver(RegObserver):
    promotionService = PromotionService()  # 依赖注入

    def handle_reg_success(self, user_id):
        self.promotionService.issueNewUserExperienceCash(user_id)


class RegNotificationObserver(RegObserver):
    notificationService = NotificationService()  # 依赖注入

    def handle_reg_success(self, user_id):
        self.notificationService.sendInboxMessage(user_id, "Welcome...")


class UserController:
    userService = UserService()  # 依赖注入
    regObservers: typing.List[RegObserver] = []

    #   一次性设置好，之后也不可能动态的修改
    def set_reg_observers(self, observers: typing.List[RegObserver]):
        self.regObservers.extend(observers)

    def register(self, telephone: str, password: str):
        user_id = UserService.register(telephone, password)
        for observer in self.regObservers:
            observer.handle_reg_success(user_id)
        return user_id
