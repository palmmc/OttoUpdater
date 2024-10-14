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
import os
import shutil
import json


class OttoUpdater(Plugin):
    prefix = "OttoUpdater"
    api_version = "0.5"
    load = "POSTWORLD"

    def on_enable(self) -> None:
        self.register_events(self)

    updateCount = 0

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
        self.updateCount = len(plugins)
        if self.updateCount == 0:
            self.logger.info(
                f"{ColorFormat.BOLD}Looks like you're all caught up!{ColorFormat.RESET}"
            )
            self.logger.info(
                "No plugin updates were found, but I can only detect plugins containing a GitHub URL, so if you are having problems, make sure to double check your plugins manually!\n"
            )
        else:
            self.logger.info(
                f"{ColorFormat.BOLD}Updates available: {ColorFormat.DARK_GRAY}({ColorFormat.RED}{self.updateCount}{ColorFormat.DARK_GRAY}){ColorFormat.RESET}"
            )
        for plugin in plugins:
            latest_version = plugin["latest_version"]
            local_version = plugin["version"]
            name = plugin["url"].split("/")[4]
            self.logger.info(
                f"{ColorFormat.GREEN}Update available for {ColorFormat.LIGHT_PURPLE}{name}{ColorFormat.GREEN}: {ColorFormat.MATERIAL_DIAMOND}{local_version} {ColorFormat.WHITE}-> {ColorFormat.DARK_AQUA}{latest_version}{ColorFormat.RESET}"
            )
            self.logger.info(
                f" > {ColorFormat.MINECOIN_GOLD}Found at {ColorFormat.BLUE}{plugin["url"]}/releases/latest{ColorFormat.RESET}"
            )
            self.logger.info(
                f"{ColorFormat.ITALIC}{ColorFormat.MATERIAL_REDSTONE}Attempting to update automagically...{ColorFormat.RESET}"
            )
            download_url = self.get_download_url(plugin)
            if not download_url:
                self.logger.error(f"Failed to fetch download for {name}.")
                continue
            self.logger.info(
                f"{ColorFormat.DARK_BLUE}Found matching file.{ColorFormat.RESET}"
            )
            new_path = self.download_file(download_url, self.pluginsPath)
            self.replace_old_file(new_path)
            self.logger.info(
                f"{ColorFormat.GREEN}Update successful: {ColorFormat.LIGHT_PURPLE}{name}{ColorFormat.GREEN}!{ColorFormat.RESET}"
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

    pluginsPath = os.path.abspath("./plugins/")

    def get_download_url(self, plugin):
        parts = plugin["url"].split("/")
        owner = parts[3]
        repo = parts[4]
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()
        result = response.json()
        response2 = requests.get(result["assets_url"])
        response2.raise_for_status()
        result = response2.json()
        resultUrl = result[0]["browser_download_url"]
        if resultUrl.endswith(".whl"):
            return resultUrl
        else:
            return None

    def download_file(self, url, dest_folder):
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = url.split("/")[-1]

        file_path = os.path.join(dest_folder, filename)

        # Save the downloaded file
        with open(file_path, "wb") as file:
            shutil.copyfileobj(response.raw, file)

        return file_path

    def replace_old_file(self, new_file_path):
        # Find and delete the old file
        old_file_path = None
        for file in os.listdir(self.pluginsPath):
            if file.endswith(".whl"):
                old_file_path = os.path.join(self.pluginsPath, file)
                break

        if old_file_path and os.path.exists(old_file_path):
            os.remove(old_file_path)

        # Move the new file to the directory
        shutil.move(
            new_file_path,
            os.path.join(self.pluginsPath, os.path.basename(new_file_path)),
        )

    @event_handler
    def on_enable(self) -> None:
        if self.updateCount > 0:
            self.logger.info(
                f"{ColorFormat.BOLD}{ColorFormat.RED}{self.updateCount} {ColorFormat.GRAY}updates applied.{ColorFormat.RESET}"
            )
            self.logger.info(
                f"{ColorFormat.YELLOW}Please run {ColorFormat.GOLD}/reload {ColorFormat.YELLOW}or re-launch for changes to take effect.{ColorFormat.RESET}"
            )
