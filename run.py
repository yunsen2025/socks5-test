import requests
from concurrent.futures import ThreadPoolExecutor

TEST_URL = "http://httpbin.org/ip"  # 公开测试地址，返回访问者IP，适合测试代理

INPUT_FILE = "s5.txt"
OUTPUT_FILE = "working_proxies.txt"

TIMEOUT = 8  # 秒
MAX_WORKERS = 10  # 并发线程数，适当调节


def test_proxy(proxy):
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    try:
        resp = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if resp.status_code == 200:
            print(f"[OK] {proxy}")
            return proxy
        else:
            print(f"[FAIL-{resp.status_code}] {proxy}")
    except Exception as e:
        print(f"[ERR] {proxy} - {e}")
    return None


def main():
    with open(INPUT_FILE, "r") as f:
        proxy_list = [line.strip() for line in f if line.strip()]

    working_proxies = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = executor.map(test_proxy, proxy_list)

        for r in results:
            if r:
                working_proxies.append(r)

    with open(OUTPUT_FILE, "w") as f:
        for proxy in working_proxies:
            f.write(proxy + "\n")

    print(f"\n检测完成！可用代理共计：{len(working_proxies)}条，已保存到 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
