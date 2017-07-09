
route_dict = {}


def map_route(uri_template, resource):
    global route_dict

    route_dict[uri_template] = resource


def get_route(uri_template):
    return route_dict[uri_template]
