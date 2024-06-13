from dotenv import load_dotenv, find_dotenv


def load_env():
    env_path = find_dotenv()
    load_dotenv(dotenv_path=env_path, verbose=True, override=True)
