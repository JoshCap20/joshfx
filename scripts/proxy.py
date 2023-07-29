import random

from proxies import proxies, user_agents


def get_random_proxy() -> dict[str, str]:
    return {
        "socks4": random.choice(proxies)
    }


def get_random_user_agent() -> dict[str, str]:
    return {
        "User-Agent": random.choice(user_agents)
    }
