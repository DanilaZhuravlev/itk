import aiohttp
import asyncio
import json

semaphore = asyncio.Semaphore(5)

async def fetch_status(url):
    async with semaphore:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return response.status
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            return 0

async def fetch_urls(urls: list[str], results_file_path: str) -> dict:
    status_codes = {}

    tasks = [fetch_status(url) for url in urls]
    results = await asyncio.gather(*tasks)

    for url, result in zip(urls, results):
        status_codes[url] = result

    all_results = []
    for url, status_code in status_codes.items():
        output_data = {"url": url, "status_code": status_code}
        all_results.append(output_data)

    with open(results_file_path, 'w') as f:
        json.dump(all_results, f, indent=4)

    print(f"Результаты сохранены в {results_file_path}")
    return status_codes

async def main():
    urls = [
        "https://example.com",
        "https://httpbin.org/status/404",
        "https://nonexistent.url"
    ]
    results_file = 'results.json'
    results_dict = await fetch_urls(urls, results_file)
    print("Словарь результатов:", results_dict)


if __name__ == "__main__":
    asyncio.run(main())