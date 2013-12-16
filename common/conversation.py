from protorpc import messages

class WorkerRequest(messages.Message):
    message = messages.StringField(1, required=True)

class WorkerResponse(messages.Message):
    message = messages.StringField(1, required=True)

