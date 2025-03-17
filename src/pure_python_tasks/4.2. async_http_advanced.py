import aiohttp
import asyncio
import json

semaphore = asyncio.Semaphore(5)

async def fetch_json_content(url: str) -> dict or None:
    async with semaphore:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        try:
                            json_content = await response.json()
                            return json_content
                        except aiohttp.ContentTypeError:
                            print(f"Ошибка: Ответ от {url} не в формате JSON")
                            return None
                    else:
                        print(f"Ошибка: Статус код для {url}: {response.status}")
                        return None
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Ошибка соединения для {url}: {e}")
            return None

async def read_urls_from_file(file_path: str) -> list[str]:
    urls = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                url = line.strip()
                if url:
                    urls.append(url)
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден: {file_path}")
        return []
    return urls

async def fetch_urls(urls_file_path: str, results_file_path: str) -> dict:
    contents = {}

    urls = await read_urls_from_file(urls_file_path)
    if not urls:
        print("Нет URL для обработки.")
        return contents

    tasks = [fetch_json_content(url) for url in urls]
    results = await asyncio.gather(*tasks)

    for url, result in zip(urls, results):
        if result:
            contents[url] = result

    with open(results_file_path, 'a') as f:
        for url, content in contents.items():
            output_data = {"url": url, "content": content}
            json_string = json.dumps(output_data)
            await asyncio.to_thread(f.write, json_string + '\n')

    print(f"Результаты сохранены в {results_file_path}")
    return contents

async def main():
    urls_file = '../urls.txt'
    results_file = 'result.jsonl'
    results_dict = await fetch_urls(urls_file, results_file)
    print("Словарь результатов:", results_dict)

if __name__ == "__main__":
    asyncio.run(main())