from werkzeug.middleware.proxy_fix import ProxyFix

from books.app import create_app
from books.config import dev_config


app = create_app(dev_config)

app.wsgi_app = ProxyFix(app.wsgi_app)


if __name__ == '__main__':
    app.run('0.0.0.0')
