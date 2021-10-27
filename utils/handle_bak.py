# coding: utf-8
import subprocess
import os
import time


def get_deploy_replicas(namespace):
    cmd = "kubectl get deploy  -n %s |  awk '{print $3}'   |grep -v 'UP-TO-DATE'" % namespace
    res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    deploy_replicas = []
    for line in res.stdout.readlines():
        deploy_replicas.append(line.decode("utf-8").strip())
    return deploy_replicas


def get_deploy_replicas_by_deploy_name(namespace, deploys):
    deploy_replicas = []
    if len(deploys) > 0:
        for i in range(len(deploys)):
            cmd = "kubectl get deploy %s -n %s |  awk '{print $3}' |grep -v 'UP-TO-DATE'" % (deploys[i], namespace)
            res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            for line in res.stdout.readlines():
                deploy_replicas.append(line.decode("utf-8").strip())
    return deploy_replicas


def get_deploy_name(namespace, keyword):
    if keyword:
        cmd = "kubectl get deploy  -n %s |  awk '{print $1}'   |grep -v 'NAME' |grep %s" % (namespace, keyword)
    else:
        cmd = "kubectl get deploy  -n %s |  awk '{print $1}'   |grep -v 'NAME'" % namespace
    res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    deploy_names = []
    for line in res.stdout.readlines():
        deploy_names.append(line.decode("utf-8").strip())
    return deploy_names


def restart_k8s_deploy_by_namespce(namespace):
    namespace = namespace
    deploy_replicas = get_deploy_replicas(namespace=namespace)
    deploy_names = get_deploy_name(namespace=namespace, keyword=None)
    result = ""
    try:
        if len(deploy_replicas) == len(deploy_names) != 0:
            for i in range(len(deploy_replicas)):
                sleep_time = int(deploy_replicas[i])
                if sleep_time > 0:
                    cmd = "kubectl get deploy  -n {} {}".format(namespace, deploy_names[i])
                    os.system(cmd)
                    time.sleep(sleep_time)
            result = '%s命名空间重启完成' % namespace
    except Exception as e:
        result = '{}命名空间重启出错:{}'.format(namespace, e)
    return result


def restart_k8s_deploy_by_keyword(namespace, keyword):
    deploy_names = get_deploy_name(namespace=namespace, keyword=keyword)
    deploy_replicas = get_deploy_replicas_by_deploy_name(namespace=namespace, deploys=deploy_names)
    result = ""
    try:
        if len(deploy_replicas) == len(deploy_names) != 0:
            for i in range(len(deploy_replicas)):
                sleep_time = int(deploy_replicas[i])
                if sleep_time > 0:
                    cmd = "kubectl get deploy  -n {} {}".format(namespace, deploy_names[i])
                    os.system(cmd)
                    time.sleep(sleep_time)
            result = '%s命名空间带有%s字样的服务重启完成' % (namespace, keyword)
    except Exception as e:
        result = '{}命名空间重启出错:{}'.format(namespace, e)
    return result


def restart_k8s_deploy_by_name(namespace, name):
    cmd = "kubectl get deploy  -n {} {}".format(namespace, name)
    print(cmd)
    res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    deploy_name = []
    for line in res.stdout.readlines():
        deploy_name.append(line.decode("utf-8").strip())
    if len(deploy_name) == 0:
        result = "发生错误，请检查命名空间或deploy名称是否正确"
    else:
        cmd = "kubectl get deploy  -n {} {}".format(namespace, name)
        res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        deploy_name = []
        for line in res.stdout.readlines():
            deploy_name.append(line.decode("utf-8").strip())
            print(deploy_name[0])
        result = "{}已重启".format(name)
    return result


