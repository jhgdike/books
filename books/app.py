from flask import Flask


def create_app(config):
    flask_app = Flask('books')
    flask_app.config.update(config)
    flask_app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    from books.ext import ext_list
    for flask_ext in ext_list:
        flask_ext.init_app(flask_app)

    from books.source.views import bp_list
    for bp in bp_list:
        flask_app.register_blueprint(bp)
    return flask_app


if __name__ == '__main__':
    from books.config import dev_config
    app = create_app(dev_config)
    app.run('0.0.0.0')
