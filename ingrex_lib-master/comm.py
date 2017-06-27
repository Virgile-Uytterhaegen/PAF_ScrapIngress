"COMM monitor"
import ingrex
import time

def main():
    "main function"
    field = {
        'minLngE6':234746932,
        'minLatE6':488260510,
        'maxLngE6':235755443,
        'maxLatE6':488308821,

    }
    with open('cookies') as cookies:
        cookies = cookies.read().strip()

    mints = -1

    while True:
        intel = ingrex.Intel(cookies, field)
        result = intel.fetch_msg(mints)
        if result:
            mints = result[0][1] + 1
        for item in result[::-1]:
            message = ingrex.Message(item)
            print(u'{} {}'.format(message.time, message.text))
        time.sleep(10)

if __name__ == '__main__':
    main()
