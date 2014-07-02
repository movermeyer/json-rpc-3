from proxy import Proxy, RequestError

endpoint = ('127.0.0.1', 4000)


def main():
    proxy = Proxy(endpoint)
    print(proxy.simple_add(first=17, second=39))
    print(proxy.echo("Hello!"))
    print(proxy.dict_to_list({1: 3, 'two': 'string', 3: [5, 'list', {'c': 0.3}]}))

    try:
        print(proxy.subtract(1, 2, 3))
    except RequestError:
        print("Got exception")


if __name__ == "__main__":
    main()
