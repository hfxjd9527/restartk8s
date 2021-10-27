from flask import Flask
from utils import handle
app = Flask(__name__)


@app.route('/k8s/restart/namespace/<namespace>')
def restart_namespace(namespace):
    res = handle.restart_k8s_deploy_by_namespce(namespace=namespace)
    print(res)
    return res


@app.route('/k8s/restart/deployment/<namespace>/<deployment>')
def restart_deploy(namespace, deployment):
    res = handle.restart_k8s_deploy_by_name(namespace=namespace, name=deployment)
    print(res, type(res))
    return res


@app.route('/k8s/restart/keyword/<namespace>/<keyword>')
def restart_keyword(namespace, keyword):
    res = handle.restart_k8s_deploy_by_keyword(namespace=namespace, keyword=keyword)
    print(res)
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5107)

