"""
This script runs the experta_server application using a development server.
"""

import os

from flasgger import Swagger

from core.config import app
from core.routes.facts import api_facts, api_rules

app.config['SWAGGER'] = {
    'swagger':'2.0',
    'ui_params_text': '''{
        "operationsSorter" : function (a, b) {
            var order = {'get': '0', 'put': '1', 'post': '2', 'delete': '3'};
            return order[a.get("method")].localeCompare(order[b.get("method")]);
        }
    }''',
    'securityDefinitions': {
        'Basic': {
            'type': 'oauth2',
            'flow': 'password',
            'description': 'Authorization',
            'tokenUrl': 'http://localhost:49153/api/login'
        }
    }
}

@app.route('/')
def hello():
    return 'Hello, API v1! Server Experta'

app.register_blueprint(api_facts)
app.register_blueprint(api_rules)

config = Swagger.DEFAULT_CONFIG
# config['swagger_ui_bundle_js'] = '/static/swagger-ui-bundle.js'
swagger = Swagger(app, config)  # template=

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 38080)), debug=True)
