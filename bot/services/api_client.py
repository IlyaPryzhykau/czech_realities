import httpx
from bot.config import API_BASE_URL


async def get_categories() -> list[dict]:
    """
    Fetches the list of categories from the API.
    Returns a list of dictionaries (one dict per category).
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(f'{API_BASE_URL}/category')
        resp.raise_for_status()
        return resp.json()


async def get_topics() -> list[dict]:
    """
    Fetches the list of topics from the API.
    Returns a list of dictionaries (one dict per topic).
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(f'{API_BASE_URL}/topic/')
        resp.raise_for_status()
        return resp.json()


async def get_questions_by_topic(topic_id: int) -> list[dict]:
    """
    Fetches all questions related to the specified topic.
    Returns a list of dictionaries (one dict per question).
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(f'{API_BASE_URL}/question/by-topic/{topic_id}')
        resp.raise_for_status()
        return resp.json()


async def get_random_question() -> dict:
    """
    Fetches a single random question from the API.
    Returns a dictionary with question data.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(f'{API_BASE_URL}/question/random-one')
        resp.raise_for_status()
        return resp.json()


async def get_random_ticket() -> list[dict]:
    """
    Fetches a random set of questions (ticket) from the API.
    Returns a list of dictionaries (one dict per question).
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(f'{API_BASE_URL}/question/random-ticket')
        resp.raise_for_status()
        return resp.json()
