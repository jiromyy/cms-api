from pydantic import BaseModel

# TODO: move this to the config folder/directory
class AppConfigValues(BaseModel):
    config_values: dict
