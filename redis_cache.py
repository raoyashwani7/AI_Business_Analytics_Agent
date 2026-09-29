import os
import redis
import json

REDIS_URL = os.getenv("REDIS_URL")

if REDIS_URL:
    redis_client = redis.from_url(
        REDIS_URL,
        decode_responses=True
    )
else:
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )


def get_cached_answer(question: str):
    try:
        key = f"business_question:{question.strip().lower()}"
        cached = redis_client.get(key)

        if cached:
            return json.loads(cached)

    except redis.exceptions.ConnectionError:
        return None

    return None


def cache_answer(question: str, answer: str):
    try:
        key = f"business_question:{question.strip().lower()}"

        redis_client.setex(
            key,
            3600,
            json.dumps(answer)
        )

    except redis.exceptions.ConnectionError:
        pass