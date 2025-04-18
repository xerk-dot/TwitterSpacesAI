from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser
from pydantic import SecretStr
from pydantic import BaseModel

from browser_use import Agent, ActionResult, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig

import os
import asyncio
from dotenv import load_dotenv
import json
import os.path
from datetime import datetime

load_dotenv()


async def create_list(name = "my_list"):

    browser = Browser()
    initial_actions = [
        {'open_tab': {'url': 'https://x.com/i/lists/create'}},
    ]

    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'twitter_cookies.txt')

    context = BrowserContext(browser=browser, config=BrowserContextConfig(cookies_file=file_path))

    controller = Controller()
    agent = Agent(
        task=(
            "Create a new list. Name the list: " + name + ". Make it private. Create it."
        ),
        llm=ChatOpenAI(model="gpt-4o"),
        save_conversation_path="logs/conversation",  # Save chat logs
		browser_context=context,
        initial_actions=initial_actions,
        max_actions_per_step=4,
        controller=controller
    )
    history = await agent.run(max_steps=10)
    await browser.close()

    return True

if __name__ == "__main__":
    create_list()