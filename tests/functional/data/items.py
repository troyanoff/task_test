from http import HTTPStatus

endpoints_v1_protected = [
    # auth
    ('api/v1/auth/login', 'post', HTTPStatus.UNPROCESSABLE_ENTITY),
    # ('api/v1/auth/logout', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/auth/refresh', 'get', HTTPStatus.UNAUTHORIZED),
    # users
    ('api/v1/users/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/users/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/users/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/users/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/users/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/users/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    # clients
    ('api/v1/clients/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/clients/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/clients/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/clients/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/clients/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/clients/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    # companies
    ('api/v1/companies/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/companies/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/companies/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/companies/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/companies/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/companies/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    # locations
    ('api/v1/locations/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/locations/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/locations/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/locations/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/locations/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/locations/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    # instructors
    ('api/v1/instructors/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/instructors/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/instructors/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/instructors/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/instructors/archive', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/instructors/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/instructors/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    # actions
    ('api/v1/actions/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/actions/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/actions/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/actions/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/actions/archive', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/actions/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/actions/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    # cards
    ('api/v1/cards/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/cards/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/cards/add_events', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/cards/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/cards/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/cards/archive', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/cards/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/cards/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    # events
    ('api/v1/events/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/events/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/events/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/events/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/events/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/events/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    # subscriptions
    ('api/v1/subscriptions/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/subscriptions/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/subscriptions/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/subscriptions/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/subscriptions/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/subscriptions/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    # issuances
    ('api/v1/issuances/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/issuances/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/issuances/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/issuances/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/issuances/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/issuances/actuals', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/issuances/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    # timeslots
    ('api/v1/timeslots/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/timeslots/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/timeslots/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/timeslots/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/timeslots/cancel', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/timeslots/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/timeslots/get_by_filter', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/timeslots/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/timeslots/get_by_location', 'get', HTTPStatus.UNAUTHORIZED),
    # records
    ('api/v1/records/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/records/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/records/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/records/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/records/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/records/get_many', 'post', HTTPStatus.UNAUTHORIZED),
]

endpoints_v1_protected_admin = [
    # auth
    # users
    ('api/v1/users/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/users/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/users/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/users/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/users/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/users/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    # clients
    ('api/v1/clients/', 'delete', HTTPStatus.UNAUTHORIZED),
    # companies
    # locations
    # instructors
    ('api/v1/instructors/', 'delete', HTTPStatus.UNAUTHORIZED),
    # actions
    ('api/v1/actions/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/actions/', 'delete', HTTPStatus.UNAUTHORIZED),
    # cards
    ('api/v1/cards/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/cards/', 'delete', HTTPStatus.UNAUTHORIZED),
    # events
    ('api/v1/events/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/events/', 'delete', HTTPStatus.UNAUTHORIZED),
    # subscriptions
    ('api/v1/subscriptions/', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/subscriptions/', 'post', HTTPStatus.UNAUTHORIZED),
    ('api/v1/subscriptions/', 'patch', HTTPStatus.UNAUTHORIZED),
    ('api/v1/subscriptions/', 'delete', HTTPStatus.UNAUTHORIZED),
    ('api/v1/subscriptions/get', 'get', HTTPStatus.UNAUTHORIZED),
    ('api/v1/subscriptions/get_many', 'post', HTTPStatus.UNAUTHORIZED),
    # issuances
    ('api/v1/issuances/', 'patch', HTTPStatus.UNAUTHORIZED),
    # timeslots
    ('api/v1/timeslots/', 'delete', HTTPStatus.UNAUTHORIZED),
    # records
    ('api/v1/records/', 'patch', HTTPStatus.UNAUTHORIZED),
]
