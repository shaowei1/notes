import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(f"{BASE_DIR}/app/")

from engine.configs import db, application

from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager

# NOTE: 奇怪的操作, 当导入一个model后, 会自动发现其他的model
#       而不导入时, 任何model都不会被发现
from accounts.models import BillingAccount

migrate = Migrate(application, db)
manager = Manager(application)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    # manager.run()
    pass