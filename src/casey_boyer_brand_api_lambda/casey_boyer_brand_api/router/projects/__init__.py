from http_router import Router

from casey_boyer_brand_api.router.projects.strate_go import router_strate_go

router_projects = Router(trim_last_slash=True)

router_projects.route("/strate-go")(router_strate_go)
