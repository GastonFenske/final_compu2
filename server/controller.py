from router import route

# TODO: this is not working as expected, just because it is in another file, but if it is in the same file it works
@route('/api/open_markets', 'GET')
def get_open_markets():
    return {'open_markets': 'some open markets'}