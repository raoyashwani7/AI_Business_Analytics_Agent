import redis
import json

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def get_cached_answer(question: str):
    key = f"business_question:{question.strip().lower()}"

    cached = redis_client.get(key)

    if cached:
        return json.loads(cached)

    return None


def cache_answer(question: str, answer: str):
    key = f"business_question:{question.strip().lower()}"

    redis_client.setex(
        key,
        3600,
        json.dumps(answer)
    )