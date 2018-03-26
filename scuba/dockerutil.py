import subprocess
import errno
import json
import re
import os

class DockerError(Exception):
    pass

class DockerExecuteError(DockerError):
    pass

class NoSuchImageError(DockerError):
    def __init__(self, image):
        self.image = image

    def __str__(self):
        return 'No such image: {}'.format(self.image)

class NoSuchContainerError(DockerError):
    def __init__(self, container):
        self.container = container

    def __str__(self):
        return 'No such container: {0}'.format(self.container)


def __wrap_docker_exec(func):
    '''Wrap a function to raise DockerExecuteError on ENOENT'''
    def call(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise DockerExecuteError('Failed to execute docker. Is it installed?')
            raise
    return call

Popen = __wrap_docker_exec(subprocess.Popen)
call  = __wrap_docker_exec(subprocess.call)


def docker_inspect(image):
    '''Inspects a docker image

    Returns: Parsed JSON data
    '''
    args = ['docker', 'inspect', '--type', 'image', image]
    p = Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    stdout, stderr = p.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    if not p.returncode == 0:
        if 'no such image' in stderr.lower():
            raise NoSuchImageError(image)
        raise DockerError('Failed to inspect image: {}'.format(stderr.strip()))

    return json.loads(stdout)[0]

def docker_inspect_container(container):
    '''Inspects a docker container

    Returns: Parsed JSON data
    '''
    args = ['docker', 'inspect', container]
    p = Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    stdout, stderr = p.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    if not p.returncode == 0:
        if 'no such object' in stderr.lower():
            raise NoSuchContainerError(container)
        raise DockerError('Failed to inspect container: {0}'.format(stderr.strip()))

    return json.loads(stdout)[0]

def docker_pull(image):
    '''Pulls an image'''
    args = ['docker', 'pull', image]

    # If this fails, the default docker stdout/stderr looks good to the user.
    ret = call(args)
    if ret != 0:
        raise DockerError('Failed to pull image "{}"'.format(image))

def docker_inspect_or_pull(image):
    '''Inspects a docker image, pulling it if it doesn't exist'''
    try:
        return docker_inspect(image)
    except NoSuchImageError:
        # If it doesn't exist yet, try to pull it now (#79)
        docker_pull(image)
        return docker_inspect(image)

def get_image_command(image):
    '''Gets the default command for an image'''
    info = docker_inspect_or_pull(image)
    try:
        return info['Config']['Cmd']
    except KeyError as ke:
        raise DockerError('Failed to inspect image: JSON result missing key {}'.format(ke))

def get_image_entrypoint(image):
    '''Gets the image entrypoint'''
    info = docker_inspect_or_pull(image)
    try:
        return info['Config']['Entrypoint']
    except KeyError as ke:
        raise DockerError('Failed to inspect image: JSON result missing key {}'.format(ke))


def make_vol_opt(hostdir, contdir, options=None):
    '''Generate a docker volume option'''
    vol = '--volume={}:{}'.format(hostdir, contdir)
    if options != None:
        if isinstance(options, str):
            options = (options,)
        vol += ':' + ','.join(options)
    return vol

def get_my_container_id(proc_file = '/proc/self/cgroup'):
    '''Get ID of container I am running in (None if not running in container)'''
    with open(proc_file, 'r') as fh:
        cgroup_data = fh.read()
    cgroup_names = ['docker']
    container_id = None
    for name in cgroup_names:
        match = re.match(r'\d+:[0-9a-zA-Z=,_\.]*:/' + name + r'/([0-9a-zA-Z]{64})$', cgroup_data, re.MULTILINE)
        if match:
            container_id = match.group(1)
            break
    # No matches is not an error. Just means we are not running in container
    return container_id

def get_path_mount(path, container_id = ''):
    if container_id == '':
        container_id = get_my_container_id()
    host_path = mount_path = None
    rel_path = None
    mount_options = None
    if container_id == None:
        host_path = mount_path = path
        return (host_path, mount_path, rel_path, mount_options)
    info = docker_inspect_container(container_id)
    mounts = info['Mounts']
    for mount in mounts:
        p = os.path.relpath(path, mount['Destination'])
        if not p.startswith('..'):
            mount_path = mount['Destination']
            rel_path = p
            mount_options = mount['Mode']
            if mount['Type'] == 'volume':
                host_path = mount['Name']
            elif mount['Type'] == 'bind':
                host_path = mount['Source']
            else:
                raise DockerError("Unsupported mount type {0}".format(mount['Type']))
            break

    if not host_path:
        raise DockerError("Running inside docker, but path {0} is not a volume so cannot create sibling container".format(path))

    return (host_path, mount_path, rel_path, [mount_options])
