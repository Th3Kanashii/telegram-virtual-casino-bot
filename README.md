# 🎰️ Virtual Casino in Telegram 📱

[![Telegram Bot](https://img.shields.io/badge/Telegram-@BaacharuKajino-blue)](https://t.me/BaacharuKajino_bot)

Virtual Casino is a transparent casino based on animated Telegram emoji.
A bot was created for the demonstration [@BaacharuKajino](https://t.me/BaacharuKajino_bot)

## System dependencies

- Python 3.11+
- Docker
- docker-compose
- make
- poetry

## Deployment

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Th3Kanashii/telegram-virtual-casino-bot.git
    ```

2. **Rename `.env.dist` to `.env` and configure it:**

   Rename the `.env.dist` file to `.env` and specify the necessary parameters for the bot to work.

3. **Build the application and run the bot:**

    Execute the following commands:

    ```bash
    make app-build
    make app-run
    ```

## Development

### Setup environment

```bash
poetry install
```

### Update database tables structure

**Make migration script:**

```bash
make migration message=MESSAGE_WHAT_THE_MIGRATION_DOES rev_id=ID_MIGRATION
```

**Run migrations:**

```bash
make migrate
```

### Update locales

1. Parse new used localization keys to update locales files
   (`make i18n locale=TRANSLATION_LOCALE`)
2. Write new locales in `.ftl` files by `translations/TRANSLATION_LOCALE`
3. Restart the bot

## Used technologies

- [Aiogram 3.x](https://github.com/aiogram/aiogram) (Telegram bot framework)
- [PostgreSQL](https://www.postgresql.org/) (database)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (working with database from Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (lightweight database migration tool)
- [Redis](https://redis.io/docs/) (in-memory data storage for FSM and caching)
- [Project Fluent](https://projectfluent.org/) (modern localization system)
