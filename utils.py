def contains_instance(obj, classes):
    for a_class in classes:
        if isinstance(obj, a_class):
            return True
    return False
