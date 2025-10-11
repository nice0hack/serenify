import pkgutil
import importlib

__all__ = []

for module_info in pkgutil.iter_modules(__path__):
    module_name = module_info.name
    module = importlib.import_module(f"{__name__}.{module_name}")

    # Добавляем в глобальное пространство все объекты из модуля
    for attr in dir(module):
        if not attr.startswith("_"):  # Пропускаем служебные переменные
            globals()[attr] = getattr(module, attr)
            __all__.append(attr)

# SClinicInServiceOut.model_rebuild()
# SServicesInClinicOut.model_rebuild()