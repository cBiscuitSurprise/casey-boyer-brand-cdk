from casey_boyer_brand_api.router import router


class TestBasicRouteMatching:
    def test_health_check(self):
        assert router("/api/health-check", "GET")
    
    def test_contact(self):
        assert router("/api/contact", "POST")

    def test_projects_strate_go_connect(self):
        assert router("/api/projects/strate-go/connect", "GET")
