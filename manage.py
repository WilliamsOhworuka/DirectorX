from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from models import db, Movie, Actor

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# custom seed command
@manager.command
def seed():
    Movie(title='Terminator', release_date='2019-09-23').insert()
    Movie(title='Sonic', release_date='2020-01-01').insert()

    Actor(name='Arnold schwarzenegger', age=72, gender='male').insert()
    Actor(name='Natalia Reyes Gaitán', age=33, gender='female').insert()
    Actor(name='Tika Sumpter', age=39, gender='female').insert()
    Actor(name='James Paul Marsden', age=46, gender='male').insert()

if __name__ == '__main__':
    manager.run()