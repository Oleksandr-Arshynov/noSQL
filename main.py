from typing import Any
import redis
from redis_lru import RedisLRU
from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


if __name__ == '__main__':
    while True:
        command = input("Enter command (name/tag): ").strip()
        
        # Перевіряємо, чи команда має префікс "name:"
        if command.startswith('name:'):
            author_name = command.split(':')[1].strip()
            # Перевіряємо, чи результат пошуку вже є в кеші Redis
            if client.exists(author_name):
                # Отримуємо результат з кешу
                quotes = client.get(author_name)
                print(f"Quotes for author '{author_name}' from cache:")
                print(quotes.decode())
            else:
                # Виконуємо пошук у MongoDB
                quotes = find_by_author(author_name)
                print(f"Quotes for author '{author_name}':")
                for quote in quotes:
                    print(quote)
                # Зберігаємо результат у кеші Redis
                client.set(author_name, '\n'.join(quotes))
        
        # Перевіряємо, чи команда має префікс "tag:"
        elif command.startswith('tag:'):
            tag = command.split(':')[1].strip()
            # Перевіряємо, чи результат пошуку вже є в кеші Redis
            if client.exists(tag):
                # Отримуємо результат з кешу
                quotes = client.get(tag)
                print(f"Quotes for tag '{tag}' from cache:")
                print(quotes.decode())
            else:
                # Виконуємо пошук у MongoDB
                quotes = find_by_tag(tag)
                print(f"Quotes for tag '{tag}':")
                for quote in quotes:
                    print(quote)
                # Зберігаємо результат у кеші Redis
                client.set(tag, '\n'.join(quotes))
    
    else:
        print("Invalid command")
