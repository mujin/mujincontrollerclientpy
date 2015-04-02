import requests
import requests.auth

class Session(requests.Session):

    def __init__(self, baseurl, username, password):
        super(Session, self).__init__()
        self._baseurl = baseurl
        self._username = username
        self._password = password
        self._csrftoken = ''

    def request(self, *args, **kwargs):
        headers = {}
        if self._csrftoken:
            headers['X-CSRFToken'] = self._csrftoken
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers
        return super(Session, self).request(*args, **kwargs)

    def login(self):
        self.auth = requests.auth.HTTPBasicAuth(self._username, self._password)

        response = self.get('%s/login/' % self._baseurl)
        self._csrftoken = response.cookies['csrftoken']

        response = self.post('%s/login/' % self._baseurl, data={
            'username': self._username,
            'password': self._password,
            'this_is_the_login_form': '1',
            'next': '/',
        })

        if response.status_code != requests.codes.ok:
            raise ValueError(u'failed to authenticate: %r' % r.text)

