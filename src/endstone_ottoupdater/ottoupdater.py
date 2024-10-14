from typing import Callable
from endstone._internal.endstone_python import (
    ColorFormat,
    Player,
    RenderType,
)
from endstone.command import Command, CommandSender
from endstone.event import event_handler
from endstone.plugin import Plugin
import requests


class OttoUpdater(Plugin):
    prefix = "OttoUpdater"
    api_version = "0.5"
    load = "POSTWORLD"

    def on_enable(self) -> None:
        self.register_events(self)

    def on_load(self):
        # Get github urls.
        plugins = []
        for plugin in self.server.plugin_manager.plugins:
            try:
                url = plugin._get_description().website.split(", ")[1]
                if url and "github.com" in url:
                    local_version = plugin._get_description().version
                    latest_version = self.get_latest_release(url)
                    if latest_version and not local_version in latest_version:
                        plugins.append(
                            {
                                "url": url,
                                "version": local_version,
                                "latest_version": latest_version,
                            }
                        )
            except Exception as e:
                continue

        self.logger.info(
            ColorFormat.DARK_GRAY
            + """
        ___ _____ _____ ___    _   _ ___ ___   _ _____ ___ ___ 
      / _ \_   _|_   _/ _ \  | | | | _ \   \ /_\_   _| __| _ \
      
     | (_) || |   | || (_) | | |_| |  _/ |) / _ \| | | _||   /
      \___/ |_|   |_| \___/   \___/|_| |___/_/ \_\_| |___|_|_\
                                                          
               """
            + ColorFormat.GRAY
            + """Let's see what updates there are today!
            """
        )
        # Check for updates
        if len(plugins) == 0:
            self.logger.info(
                f"{ColorFormat.BOLD}Looks like you're all caught up!{ColorFormat.RESET}"
            )
            self.logger.info(
                "No plugin updates were found, but I can only detect plugins containing a GitHub URL, so if you are having problems, make sure to double check your plugins manually!\n"
            )
        else:
            self.logger.info(
                f"{ColorFormat.BOLD}Updates available: {ColorFormat.DARK_GRAY}({ColorFormat.RED}{len(plugins)}{ColorFormat.DARK_GRAY}){ColorFormat.RESET}"
            )
        for plugin in plugins:
            latest_version = plugin["latest_version"]
            local_version = plugin["version"]
            self.logger.info(
                f"{ColorFormat.GREEN}Update available for {ColorFormat.LIGHT_PURPLE}{plugin["url"].split("/")[4]}{ColorFormat.GREEN}: {ColorFormat.MATERIAL_DIAMOND}{local_version} {ColorFormat.WHITE}-> {ColorFormat.DARK_AQUA}{latest_version}{ColorFormat.RESET}"
            )
            self.logger.info(
                f" > {ColorFormat.MINECOIN_GOLD}Get it now at {ColorFormat.BLUE}{plugin["url"]}/releases/latest{ColorFormat.RESET}"
            )

    def get_latest_release(self, url: str) -> str:
        try:
            # Extract owner and repo from URL
            parts = url.split("/")
            owner = parts[3]
            repo = parts[4]
            api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            response = requests.get(api_url)
            response.raise_for_status()
            latest_release = response.json()
            return latest_release["tag_name"]
        except Exception as e:
            self.logger.error(f"Failed to fetch latest release for {url}: {e}")
            return None
