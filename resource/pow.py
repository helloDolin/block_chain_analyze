import hashlib
import time


def sha256(data):
    ''' sha256 加密 '''
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()


def main():
    start = time.perf_counter()

    data = "btc"
    n = 1
    while n < 2**32:
        test_str = data + str(n)
        hash = sha256(test_str)
        hash = sha256(hash)
        if hash.startswith('000000'):
            print(test_str)
            print(hash)
            break
        n = n + 1

    print('消耗时长：{}'.format((time.perf_counter() - start)))


if __name__ == "__main__":
    main()
