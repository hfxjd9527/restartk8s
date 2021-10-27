# coding: utf-8
from flask import Flask
from utils import handle, handle_request
app = Flask(__name__)


# get请求，重启一般的全命名空间下的服务
@app.route('/k8s/restart/namespace/<namespace>/<sleep>', methods=['GET'])
def restart_namespace(namespace, sleep):
    res = handle.restart_k8s_deploy_by_namespce(namespace=namespace, sleep=sleep)
    print(res)
    return res


# post请求，重启全命名空间下不含某些不重启的服务
@app.route('/k8s/restart/namespace', methods=['POST'])
def restart_namespace_post():
    data = handle_request.get_data_from_requst()
    namespace = data.get('namespace')
    not_restart_deploys = data.get('not_restart_deploys')
    sleep = data.get('sleep')
    res = handle.restart_k8s_deploy_by_namespce_post(namespace=namespace, not_restart_deploys=not_restart_deploys,
                                                     sleep=sleep)
    print(res)
    return res


@app.route('/k8s/restart/deployment/<namespace>/<deployment>', methods=['GET'])
def restart_deploy(namespace, deployment):
    res = handle.restart_k8s_deploy_by_name(namespace=namespace, name=deployment)
    print(res, type(res))
    return res


@app.route('/k8s/restart/keyword/<namespace>/<keyword>/<sleep>', methods=['GET'])
def restart_keyword(namespace, keyword, sleep):
    res = handle.restart_k8s_deploy_by_keyword(namespace=namespace, keyword=keyword, sleep=sleep)
    print(res)
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5107)
