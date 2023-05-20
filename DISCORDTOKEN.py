def TOKEN():
    discord_config = {}

    with open("discord_config", "r", encoding="utf-8") as f:
        configs = f.readlines()
        for config in configs:
            key, value = config.rstrip().split('=')
            discord_config[key] = value

    DISCORD_TOKEN = discord_config['DISCORD_TOKEN']
    return DISCORD_TOKEN