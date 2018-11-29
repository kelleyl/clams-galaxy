class Service(object):
    """Superclass for creating a service."""

    def __init__(self, video, miff=None):
        """Constructor for Service"""
        self.video = video
        self.miff = miff

    def run_service(self):
        pass
