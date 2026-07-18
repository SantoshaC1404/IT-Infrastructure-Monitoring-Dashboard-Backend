class AlertRepository:

    def create(self, alert): ...

    def get_open_alert(
        self,
        device_id,
        metric,
    ): ...

    def resolve_alert(
        self,
        alert,
    ): ...

    def latest(self): ...

    def unresolved(self): ...
