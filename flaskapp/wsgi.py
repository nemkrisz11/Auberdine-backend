from app import create_app

application = create_app()


@application.route('/debug')
def debug():
    return str(application.blueprints)


@application.route("/site-map")
def site_map():
    return str(application.url_map)
