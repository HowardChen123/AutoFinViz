
def get_api_key():
    try:
        with open("apikey", 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % "apikey")