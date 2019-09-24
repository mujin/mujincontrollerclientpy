#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import datetime
import argparse
from mujincontrollerclient.controllerclientbase import ControllerClient
from mujincontrollerclient import uriutils

import logging
log = logging.getLogger(__name__)


def _RunMain():
    parser = argparse.ArgumentParser(description='Run registration task on remote controller')
    parser.add_argument('--logLevel', action='store', type=str, dest='logLevel', default='INFO', help='the python log level, e.g. DEBUG, VERBOSE, ERROR, INFO, WARNING, CRITICAL [default=%(default)s]')
    parser.add_argument('--controllerUrl', action='store', type=str, dest='controllerUrl', default='http://localhost', help='controller url e.g http://controller123 [default=%(default)s]')
    parser.add_argument('--controllerUsername', action='store', type=str, dest='controllerUsername', default='mujin', help='controller username [default=%(default)s]')
    parser.add_argument('--controllerPassword', action='store', type=str, dest='controllerPassword', default='mujin', help='controller password [default=%(default)s]')
    parser.add_argument('--scenepk', action='store', type=str, dest='scenepk', default=None, help='scene primary key, if not specified, will determine from remote system [default=%(default)s]')
    parser.add_argument('--ftpHost', action='store', type=str, dest='ftpHost', default='127.0.0.1', help='ftp server hostname or ip address [default=%(default)s]')
    parser.add_argument('--ftpPort', action='store', type=int, dest='ftpPort', default=21, help='ftp server port [default=%(default)r]')
    parser.add_argument('--ftpUsername', action='store', type=str, dest='ftpUsername', default='anonymous', help='ftp username [default=%(default)s]')
    parser.add_argument('--ftpPassword', action='store', type=str, dest='ftpPassword', default='', help='ftp password [default=%(default)s]')
    parser.add_argument('--ftpPath', action='store', type=str, dest='ftpPath', default='', help='path on ftp server, if not supplied, will use home directory of the user [default=%(default)s]')
    parser.add_argument('--syncMasterFile', action='store', type=str, dest='syncMasterFile', default=None, help='if supplied, will sync this master file on FTP, e.g. /somewhere/masterfile.txt [default=%(default)s]')
    parser.add_argument('--backup', action='store_true', dest='backup', default=False, help='backup registration objects to ftp [default=%(default)s]')
    parser.add_argument('--outputFilename', action='store', type=str, dest='outputFilename', default=None, help='If supplied, will output to file specified, otherwise file will be named after task name [default=%(default)s]')
    options = parser.parse_args()

    # configure logging
    try:
        from mujincommon import ConfigureRootLogger
        ConfigureRootLogger(level=options.logLevel)
    except ImportError:
        logging.basicConfig(format='%(asctime)s %(name)s [%(levelname)s] [%(filename)s:%(lineno)s %(funcName)s] %(message)s', level=options.logLevel)


    taskType = 'registration'
    command = None
    if options.syncMasterFile:
        command = 'SyncMasterFile'
    elif options.backup:
        command = 'Backup'
    else:
        raise Exception('Have to sepecify either --syncMasterFile or --backup')
    taskName = 'registration-%s-%s' % (command.lower(), datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))

    controllerclient = ControllerClient(options.controllerUrl, options.controllerUsername, options.controllerPassword)
    controllerclient.Ping()

    # cancel previous jobs
    for job in controllerclient.GetJobs():
        if '/registration-' in job['description']:
            controllerclient.DeleteJob(job['pk'])

    # determine scenepk
    if options.scenepk is None:
        options.scenepk = uriutils.GetPrimaryKeyFromURI(controllerclient.GetConfig()['sceneuri'])

    # delete previous task
    for task in controllerclient.GetSceneTasks(options.scenepk):
        if task['tasktype'] == taskType:
            controllerclient.DeleteSceneTask(options.scenepk, task['pk'])

    # create task
    task = controllerclient.CreateSceneTask(options.scenepk, {
        'tasktype': taskType,
        'name': taskName,
        'taskparameters': {
            'command': command,
            'fileStorageInfo': {
                'type': 'ftp',
                'username': options.ftpUsername,
                'password': options.ftpPassword,
                'host': options.ftpHost,
                'port': options.ftpPort,
                'remotePath': options.ftpPath,
            },
            'remoteMasterFilePath': options.syncMasterFile,
        }
    })
    taskpk = task['pk']
    log.info('task created: %s: %s', taskpk, task['name'])


    # run task async
    jobpk = controllerclient._webclient.APICall('POST', 'job/', data={
        'scenepk': options.scenepk,
        'target_pk': taskpk,
        'resource_type': 'task',
    }, expectedStatusCode=200)['jobpk']
    log.info('job started: %s', jobpk)

    # wait for job
    startTime = time.time()
    jobProgress = None
    while True:
        job = ([j for j in controllerclient.GetJobs() if j['pk'] == jobpk] or [None])[0]
        if job is None:
            if jobProgress is not None:
                # job has been seen before, so must be done now
                break
            if time.time() - startTime > 2.0:
                # perhaps job finished too quickly
                break

            # wait a little bit and check for job again
            time.sleep(0.05)
            continue

        newProgress = (
            min(1.0, max(jobProgress[0] if jobProgress else 0.0, float(job['progress']))),
            job['status'],
            job['status_text']
        )
        if newProgress != jobProgress:
            jobProgress = newProgress
            log.info('progress %.02f%%: %s: %s', jobProgress[0] * 100.0, jobProgress[1], jobProgress[2])

        if job['status'] in ('succeeded', 'aborted'):
            break

        if job['status'] in ('lost', 'preempted'):
            raise Exception('Job has stopped unexpectedly: %s' % job['status'])

        time.sleep(0.5)

    # wait for result
    result = None
    startTime = time.time()
    while True:
        task = controllerclient.GetSceneTask(options.scenepk, taskpk)
        if len(task['binpickingresults']) > 0:
            result = controllerclient.GetBinpickingResult(task['binpickingresults'][0]['pk'])
            break
        if time.time() - startTime > 5.0:
            raise Exception('Timed out waiting for task result')

    # write result
    if not options.outputFilename:
        options.outputFilename = '%s.json' % taskName
    with open(options.outputFilename, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, separators=(',', ': '), sort_keys=True)
        f.write('\n')
    log.info('result written to: %s', options.outputFilename)


if __name__ == '__main__':
    _RunMain()
