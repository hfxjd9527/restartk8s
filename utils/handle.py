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


def restart_k8s_deploy_by_namespce(namespace, sleep):
    namespace = namespace
    sleep = int(sleep)
    deploy_replicas = get_deploy_replicas(namespace=namespace)
    deploy_names = get_deploy_name(namespace=namespace, keyword=None)
    try:
        if len(deploy_replicas) == len(deploy_names) != 0:
            for i in range(len(deploy_replicas)):
                sleep_time = int(deploy_replicas[i])
                if sleep_time > 0:
                    # cmd = "kubectl get deploy  -n {} {}".format(namespace, deploy_names[i])
                    cmd = "kubectl rollout restart deploy {} -n {}".format(deploy_names[i], namespace)
                    os.system(cmd)
                    time.sleep(sleep_time*sleep)
            result = '%s命名空间重启完成' % namespace
        else:
            result = "发生错误，请检查命名空间是否正确"
    except Exception as e:
        result = '{}命名空间重启出错:{}'.format(namespace, e)
    return result


def restart_k8s_deploy_by_namespce_post(namespace, not_restart_deploys, sleep):
    namespace = namespace
    sleep = int(sleep)
    deploy_names = get_deploy_name(namespace=namespace, keyword=None)
    deploy_replicas = get_deploy_replicas(namespace=namespace)
    mapping = dict(zip(deploy_names, deploy_replicas))
    for not_restart_deploy in not_restart_deploys:
        if not_restart_deploy in mapping:
            del mapping[not_restart_deploy]
        else:
            mapping = mapping
    final_deploy_names = list(mapping.keys())
    final_deploy_replicas = list(mapping.values())
    try:
        if len(final_deploy_replicas) == len(final_deploy_names) != 0:
            for i in range(len(final_deploy_replicas)):
                sleep_time = int(final_deploy_replicas[i])
                if sleep_time > 0:
                    # cmd = "kubectl get deploy  -n {} {}".format(namespace, deploy_names[i])
                    cmd = "kubectl rollout restart deploy {} -n {}".format(final_deploy_names[i], namespace)
                    os.system(cmd)
                    time.sleep(sleep_time*sleep)
            result = '%s命名空间重启完成' % namespace
        else:
            result = "发生错误，请检查命名空间是否正确"
    except Exception as e:
        result = '{}命名空间重启出错:{}'.format(namespace, e)
    return result


def restart_k8s_deploy_by_keyword(namespace, keyword, sleep):
    sleep = int(sleep)
    deploy_names = get_deploy_name(namespace=namespace, keyword=keyword)
    deploy_replicas = get_deploy_replicas_by_deploy_name(namespace=namespace, deploys=deploy_names)
    try:
        if len(deploy_replicas) == len(deploy_names) != 0:
            for i in range(len(deploy_replicas)):
                sleep_time = int(deploy_replicas[i])
                if sleep_time > 0:
                    # cmd = "kubectl get deploy  -n {} {}".format(namespace, deploy_names[i])
                    cmd = "kubectl rollout restart deploy {} -n {}".format(deploy_names[i], namespace)
                    os.system(cmd)
                    time.sleep(sleep_time*sleep)
            result = '{}命名空间下带有关键词{}的服务重启完成'.format(namespace, keyword)
        else:
            result = "发生错误，请检查命名空间或关键词是否正确"
    except Exception as e:
        result = '{}命名空间,带有关键词{}重启出错:{}'.format(namespace, keyword, e)
    return result


def restart_k8s_deploy_by_name(namespace, name):
    cmd = "kubectl get deploy {} -n {}".format(name, namespace)
    res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    deploy_name = []
    for line in res.stdout.readlines():
        deploy_name.append(line.decode("utf-8").strip())
    if len(deploy_name) == 0:
        result = "发生错误，请检查命名空间或deploy名称是否正确"
    else:
        cmd = "kubectl rollout restart deploy {} -n {}".format(name, namespace)
        res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        deploy_name = []
        for line in res.stdout.readlines():
            deploy_name.append(line.decode("utf-8").strip())
        result = "{}已重启".format(name)
    return result
