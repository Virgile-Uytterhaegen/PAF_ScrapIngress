import ingrex

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

    intel = ingrex.Intel(cookies, field)

    result = intel.fetch_msg(tab='faction')
    result = intel.fetch_map(['17_29630_13630_0_8_100'])
    result = intel.fetch_portal(guid='ac8348883c8840f6a797bf9f4f22ce39.16')
    result = intel.fetch_score()
    result = intel.fetch_region()
    result = intel.fetch_artifacts()
    print(result)

if __name__ == '__main__':
    main()
