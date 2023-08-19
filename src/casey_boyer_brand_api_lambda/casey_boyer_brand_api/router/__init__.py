from http_router import Router

from casey_boyer_brand_api.router.api import api

router = Router(trim_last_slash=True)

router.route("/api")(api)
