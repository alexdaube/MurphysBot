class BaseClient(object):
    def _url(self, remote_address, port, relative_path="", protocol="http"):
        return "{0}://{1}:{2}/{3}".format(protocol, remote_address, port, relative_path)

    def send_log(self, message):
        pass
