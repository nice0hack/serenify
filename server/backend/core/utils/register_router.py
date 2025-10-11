
route_registry = [] # pyright: ignore[reportAssignmentType]

def register_router(cls):
    instance = cls()
    route_registry.append(instance)
    return cls
