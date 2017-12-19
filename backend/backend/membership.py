import time

class Membership:
    name = None
    activated_at = None
    deactivated_at = None

    def __init__(self, name, activated_at=time.time()):
        self.name = name
        self.activated_at = activated_at

    def deactivate(self, deactivated_at=time.time()):
        self.deactivated_at = deactivated_at

    def is_active(self):
        return (activated_at != None and deactivated_at == None)