import logging
from logging.config import fileConfig

from alembic import context

# Alembic Config object
config = context.config

# Set up logging
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

def get_engine():
    from app import create_app
    from app.db import db
    
    app = create_app()
    with app.app_context():
        return db.engine

def get_engine_url():
    from app import create_app
    from app.db import db
    
    app = create_app()
    with app.app_context():
        return str(db.engine.url).replace('%', '%%')

def get_metadata():
    from app import create_app
    from app.db import db
    
    app = create_app()
    with app.app_context():
        return db.metadata  # Directly access metadata from your db instance

config.set_main_option('sqlalchemy.url', get_engine_url())

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=get_metadata(),
        literal_binds=True,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            process_revision_directives=process_revision_directives,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()