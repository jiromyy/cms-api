from src.config.app_config_values import AppConfigValues
from src.config.app_config_manager import AppConfigManager

def fetch_app_config(app_id: str) -> dict:
    """
    Retrieves the application configuration using a given app_id.

    Args:
        app_id (str): The application identifier used to fetch configuration.

    Returns:
        AppConfigValues: A dictionary containing the application configuration values.
    """
    app_config_dict = AppConfigManager.APP_CONFIG.get(app_id)
    if app_config_dict is None:
        raise ValueError(f"No configuration found for app_id: {app_id}")

    app_config = AppConfigValues(config_values=app_config_dict)

    return app_config