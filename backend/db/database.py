from core.config import config
from crud.internal import InternalCrud
from crud.mongodb import MongoCrud


def get_default_db():
    if config['JWT']['AUTH_DATABASE'] == 'internal':
        return InternalCrud()
    else:
        return MongoCrud(
            config['MONGO']['USERNAME'],
            config['MONGO']['PASSWORD'],
            config['MONGO']['SERVER'],
            config['MONGO']['DATABASE']
        )
