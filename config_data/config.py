from dataclasses import dataclass
from environs import Env



@dataclass
class TgBot:
    token: str              # Токен для доступа к тг-боту
    admin_ids: list[int]    # Список айдишников админов бота


@dataclass
class Config:
    tg_bot: TgBot           # Конструктор тг-бота


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        )
    )
