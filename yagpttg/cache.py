"""Кеширование запросов к API."""
import redis
import json

class RedisCacheStorage:
    """Кеширование запросов к API.

    Позволяет кешировать запросы к API и хранить контекст общения.
    """
    def __init__(self, cl = None, time = None):
        if cl != None:
            self.client = cl
        else:
            self.client = redis.Redis(host='127.0.0.1')
        if time != None and (type(time) is int or type(time) is float):
            self.time = time:
        else:
            self.time = 3600
    
    def bd(self, key, question = None, answer = None):
        key = str(key)
        exs = self.client.exists(key)
        if question == None or answer == None:
            if exs == 1:
                return json.loads(self.client.get(key))
            return None
        ans = answer['result']['alternatives'][0]['message']
        if exs == 0:
            self.client.set(key, json.dumps([question, ans]), ex = self.time)
            return "Complete"
        data = json.loads(self.client.get(key))
        data.append(question)
        data.append(ans)
        self.client.set(key, json.dumps(data), ex = self.time)
        return "Complete"