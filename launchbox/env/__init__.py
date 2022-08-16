import os

# TODO? Replace with management bridge API endpoint?
# Or is it OK for the Django plugin to rely on a predictable module path
# in the Launchbox codebase?
from config.manage.env import LBEnv as LBEnvSrc


class LBEnv:
    def get(var):
        # TODO: Replace hardcoded `envdir` used for POC.
        # Question: What will the path to env vars be?
        # Will it always be the same, or will it be configurable?
        envpath = f"envdir/{os.environ.get('WCP_ALIAS')}"
        return LBEnvSrc.dir.get(envpath, var)
