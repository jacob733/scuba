 # coding=utf-8
from __future__ import print_function

from nose.tools import *
from .utils import *
from unittest import TestCase
try:
    from unittest import mock
except ImportError:
    import mock

from types import MethodType

import json
import subprocess
import scuba.compat
import scuba.dockerutil as uut
import scuba.dockerutil

container_inspect_string = '''[
    {
        "Id": "4c3d00d1870c72d99b4f6c0828ab1456e37712d0fafc1ac6d2507bc6e39c3987",
        "Created": "2018-03-27T11:41:26.744529362Z",
        "Path": "bash",
        "Args": [],
        "State": {
            "Status": "exited",
            "Running": false,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 0,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2018-03-27T11:41:27.196032955Z",
            "FinishedAt": "2018-03-27T11:41:29.22813183Z"
        },
        "Image": "sha256:c648cd6a73969d01003f84dcb558aa19f153fdbb63f6e7bc096cf204c1d46280",
        "ResolvConfPath": "/var/lib/docker/containers/4c3d00d1870c72d99b4f6c0828ab1456e37712d0fafc1ac6d2507bc6e39c3987/resolv.conf",
        "HostnamePath": "/var/lib/docker/containers/4c3d00d1870c72d99b4f6c0828ab1456e37712d0fafc1ac6d2507bc6e39c3987/hostname",
        "HostsPath": "/var/lib/docker/containers/4c3d00d1870c72d99b4f6c0828ab1456e37712d0fafc1ac6d2507bc6e39c3987/hosts",
        "LogPath": "/var/lib/docker/containers/4c3d00d1870c72d99b4f6c0828ab1456e37712d0fafc1ac6d2507bc6e39c3987/4c3d00d1870c72d99b4f6c0828ab1456e37712d0fafc1ac6d2507bc6e39c3987-json.log",
        "Name": "/keen_meninsky",
        "RestartCount": 0,
        "Driver": "overlay2",
        "Platform": "linux",
        "MountLabel": "",
        "ProcessLabel": "",
        "AppArmorProfile": "docker-default",
        "ExecIDs": null,
        "HostConfig": {
            "Binds": null,
            "ContainerIDFile": "",
            "LogConfig": {
                "Type": "json-file",
                "Config": {}
            },
            "NetworkMode": "default",
            "PortBindings": {},
            "RestartPolicy": {
                "Name": "no",
                "MaximumRetryCount": 0
            },
            "AutoRemove": false,
            "VolumeDriver": "",
            "VolumesFrom": null,
            "CapAdd": null,
            "CapDrop": null,
            "Dns": [],
            "DnsOptions": [],
            "DnsSearch": [],
            "ExtraHosts": null,
            "GroupAdd": null,
            "IpcMode": "shareable",
            "Cgroup": "",
            "Links": null,
            "OomScoreAdj": 0,
            "PidMode": "",
            "Privileged": false,
            "PublishAllPorts": false,
            "ReadonlyRootfs": false,
            "SecurityOpt": null,
            "UTSMode": "",
            "UsernsMode": "",
            "ShmSize": 67108864,
            "Runtime": "runc",
            "ConsoleSize": [
                0,
                0
            ],
            "Isolation": "",
            "CpuShares": 0,
            "Memory": 0,
            "NanoCpus": 0,
            "CgroupParent": "",
            "BlkioWeight": 0,
            "BlkioWeightDevice": [],
            "BlkioDeviceReadBps": null,
            "BlkioDeviceWriteBps": null,
            "BlkioDeviceReadIOps": null,
            "BlkioDeviceWriteIOps": null,
            "CpuPeriod": 0,
            "CpuQuota": 0,
            "CpuRealtimePeriod": 0,
            "CpuRealtimeRuntime": 0,
            "CpusetCpus": "",
            "CpusetMems": "",
            "Devices": [],
            "DeviceCgroupRules": null,
            "DiskQuota": 0,
            "KernelMemory": 0,
            "MemoryReservation": 0,
            "MemorySwap": 0,
            "MemorySwappiness": null,
            "OomKillDisable": false,
            "PidsLimit": 0,
            "Ulimits": null,
            "CpuCount": 0,
            "CpuPercent": 0,
            "IOMaximumIOps": 0,
            "IOMaximumBandwidth": 0
        },
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay2/3c2ffa08bf46b885be9debff94b97ea1048b7b0f9792b68b3ba9aa20f7460c50-init/diff:/var/lib/docker/overlay2/a737d69e224bcbf4dc775b0ba363a4e93a6d3f511a45f2e2b24cc80c40cdaa8f/diff:/var/lib/docker/overlay2/f025bc430ffd1d9adeb41427bdcbd522d889cb1be808d8287755b5628f4caf2a/diff",
                "MergedDir": "/var/lib/docker/overlay2/3c2ffa08bf46b885be9debff94b97ea1048b7b0f9792b68b3ba9aa20f7460c50/merged",
                "UpperDir": "/var/lib/docker/overlay2/3c2ffa08bf46b885be9debff94b97ea1048b7b0f9792b68b3ba9aa20f7460c50/diff",
                "WorkDir": "/var/lib/docker/overlay2/3c2ffa08bf46b885be9debff94b97ea1048b7b0f9792b68b3ba9aa20f7460c50/work"
            },
            "Name": "overlay2"
        },
        "Mounts": [
            {
                "Type": "volume",
                "Name": "testvolume",
                "Source": "/var/lib/docker/volumes/testvolume/_data",
                "Destination": "/tester",
                "Driver": "local",
                "Mode": "z",
                "RW": true,
                "Propagation": ""
            },
            {
                "Type": "bind",
                "Source": "/home/user2",
                "Destination": "/usermount",
                "Mode": "",
                "RW": true,
                "Propagation": "rprivate"
            }
        ],
        "Config": {
            "Hostname": "4c3d00d1870c",
            "Domainname": "",
            "User": "",
            "AttachStdin": true,
            "AttachStdout": true,
            "AttachStderr": true,
            "Tty": true,
            "OpenStdin": true,
            "StdinOnce": true,
            "Env": null,
            "Cmd": [
                "bash"
            ],
            "Image": "debian:8.2",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": {}
        },
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "9f08edac4afb92186d5ad7598efb3d56e44ca756446ebd08b48a6efa3b457a04",
            "HairpinMode": false,
            "LinkLocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "Ports": {},
            "SandboxKey": "/var/run/docker/netns/9f08edac4afb",
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "",
            "Gateway": "",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "",
            "IPPrefixLen": 0,
            "IPv6Gateway": "",
            "MacAddress": "",
            "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "8c235ddd93b4786b2f91bef9c1ff85dc5d2727978b75b9b6d9bcaad64b15dea6",
                    "EndpointID": "",
                    "Gateway": "",
                    "IPAddress": "",
                    "IPPrefixLen": 0,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "",
                    "DriverOpts": null
                }
            }
        }
    }
]
'''
container_inspect_data = json.loads(container_inspect_string)

class TestDockerutil(TestCase):
    def test_get_image_command_success(self):
        '''get_image_command works'''
        assert_true(uut.get_image_command('debian:8.2'))

    def test_get_image_command_bad_image(self):
        '''get_image_command raises an exception for a bad image name'''
        assert_raises(uut.DockerError, uut.get_image_command, 'nosuchimageZZZZZZZZ')

    def test_get_image_no_docker(self):
        '''get_image_command raises an exception if docker is not installed'''

        real_Popen = subprocess.Popen
        def mocked_popen(popen_args, *args, **kw):
            assert_equal(popen_args[0], 'docker')
            popen_args[0] = 'dockerZZZZ'
            return real_Popen(popen_args, *args, **kw)

        with mock.patch('subprocess.Popen', side_effect=mocked_popen) as popen_mock:
            assert_raises(uut.DockerError, uut.get_image_command, 'n/a')

    def test__get_image_command__pulls_image_if_missing(self):
        '''get_image_command pulls an image if missing'''
        image = 'busybox:latest'

        # First remove the image
        subprocess.call(['docker', 'rmi', image])

        # Now try to get the image's Command
        result = uut.get_image_command(image)

        # Should return a non-empty string
        self.assertTrue(result)

    def test_get_image_entrypoint(self):
        '''get_image_entrypoint works'''
        result = uut.get_image_entrypoint('scuba/entrypoint-test')
        self.assertEqual(1, len(result))
        assert_str_equalish('/entrypoint.sh', result[0])

    def test_get_image_entrypoint__none(self):
        '''get_image_entrypoint works for image with no entrypoint'''
        result = uut.get_image_entrypoint('debian')
        self.assertEqual(None, result)


    def test_make_vol_opt_no_opts(self):
        assert_equal(
                uut.make_vol_opt('/hostdir', '/contdir'),
                '--volume=/hostdir:/contdir'
                )

    def test_make_vol_opt_one_opt(self):
        assert_equal(
                uut.make_vol_opt('/hostdir', '/contdir', 'ro'),
                '--volume=/hostdir:/contdir:ro'
                )

    def test_make_vol_opt_multi_opts(self):
        assert_equal(
                uut.make_vol_opt('/hostdir', '/contdir', ['ro', 'z']),
                '--volume=/hostdir:/contdir:ro,z'
                )

    def test_inspect_container_success(self):
        '''Inspect container with success'''

        container_id = container_inspect_data[0]['Id']
        def mocked_popen(popen_args, stdout = None, stderr = None):
            assert_equal(len(popen_args), 3)
            assert_equal(popen_args[0], 'docker')
            assert_equal(popen_args[1], 'inspect')
            assert_equal(popen_args[2], container_id)

            def mocked_communicate(self, stdin = None):
                return (self.stdout.read(), self.stderr.read())

            ret = type('popen_mock_obj', (), {})()
            ret.stdout = scuba.compat.StringIO(container_inspect_string)
            ret.stderr = scuba.compat.StringIO()
            ret.returncode = 0
            ret.communicate = MethodType(mocked_communicate, ret)
            return ret

        with mock.patch('scuba.dockerutil.Popen', mocked_popen) as popen_mock:
            out = uut.docker_inspect_container(container_id)
            assert_equal(out['Id'], container_id)

    def test_inspect_container_no_docker(self):
        '''Inspect container with missing docker'''

        container_id = '4c3d00d1870c72d99b4f6c0828ab1456e37712d0fafc1ac6d2507bc6e39c3987'
        real_Popen = subprocess.Popen
        def mocked_popen(popen_args, *args, **kw):
            assert_equal(popen_args[0], 'docker')
            popen_args[0] = 'dockerZZZZ'
            return real_Popen(popen_args, *args, **kw)

        with mock.patch('subprocess.Popen', side_effect=mocked_popen) as popen_mock:
            assert_raises(uut.DockerError, uut.docker_inspect_container, 'n/a')


    def test_inspect_container_no_container(self):
        '''Inspect missing container'''

        container_id = 'fd670db82f3a02a7fd15869d1bab235698dc23ca3b132f01e8fec5655f33af4d'
        def mocked_popen(popen_args, stdout = None, stderr = None):
            assert_equal(len(popen_args), 3)
            assert_equal(popen_args[0], 'docker')
            assert_equal(popen_args[1], 'inspect')
            assert_equal(popen_args[2], container_id)

            def mocked_communicate(self, stdin = None):
                print("mocked_communicate")
                return (self.stdout.read(), self.stderr.read())

            ret = type('popen_mock_obj', (), {})()
            ret.stdout = scuba.compat.StringIO('[]')
            ret.stderr = scuba.compat.StringIO('Error: No such object: {0}'.format(container_id))
            ret.returncode = 1
            ret.communicate = MethodType(mocked_communicate, ret)
            return ret

        with mock.patch('scuba.dockerutil.Popen', mocked_popen) as popen_mock:
            assert_raises(uut.NoSuchContainerError, uut.docker_inspect_container, container_id)

    def test_inspect_container_other_fail(self):
        '''Inspect failure'''

        container_id = 'fd670db82f3a02a7fd15869d1bab235698dc23ca3b132f01e8fec5655f33af4d'
        def mocked_popen(popen_args, stdout = None, stderr = None):
            assert_equal(len(popen_args), 3)
            assert_equal(popen_args[0], 'docker')
            assert_equal(popen_args[1], 'inspect')
            assert_equal(popen_args[2], container_id)

            def mocked_communicate(self, stdin = None):
                print("mocked_communicate")
                return (self.stdout.read(), self.stderr.read())

            ret = type('popen_mock_obj', (), {})()
            ret.stdout = scuba.compat.StringIO('[]')
            ret.stderr = scuba.compat.StringIO('Error: Failed')
            ret.returncode = 1
            ret.communicate = MethodType(mocked_communicate, ret)
            return ret

        with mock.patch('scuba.dockerutil.Popen', mocked_popen) as popen_mock:
            assert_raises(uut.DockerError, uut.docker_inspect_container, container_id)

    def test_get_my_container_id_no_container(self):
        '''Get container ID when not in docker'''
        cgroup_contents = '''12:devices:/user.slice
11:hugetlb:/
10:perf_event:/
9:net_cls,net_prio:/
8:cpuset:/
7:freezer:/
6:rdma:/
5:blkio:/user.slice
4:cpu,cpuacct:/user.slice
3:pids:/user.slice/user-1026.slice
2:memory:/user.slice
1:name=systemd:/user.slice/user-1026.slice/session-c1.scope
'''
        mocked_open = mock.mock_open(read_data=cgroup_contents)

        with mock.patch('__builtin__.open', mocked_open):
            assert_equal(uut.get_my_container_id(), None)

    def test_get_my_container_id_in_container(self):
        '''Get container ID when in docker'''
        cgroup_contents = '''12:devices:/docker/ebfaf125efecfe74d3a99b2d4ef584c3dc23fc290e834ff052ad87b16f5f0dbb
11:hugetlb:/docker/ebfaf125efecfe74d3a99b2d4ef584c3dc23fc290e834ff052ad87b16f5f0dbb
10:perf_event:/docker/ebfaf125efecfe74d3a99b2d4ef584c3dc23fc290e834ff052ad87b16f5f0dbb
9:net_cls,net_prio:/docker/ebfaf125efecfe74d3a99b2d4ef584c3dc23fc290e834ff052ad87b16f5f0dbb
8:cpuset:/docker/ebfaf125efecfe74d3a99b2d4ef584c3dc23fc290e834ff052ad87b16f5f0dbb
7:freezer:/docker/ebfaf125efecfe74d3a99b2d4ef584c3dc23fc290e834ff052ad87b16f5f0dbb
6:rdma:/
5:blkio:/docker/ebfaf125efecfe74d3a99b2d4ef584c3dc23fc290e834ff052ad87b16f5f0dbb
4:cpu,cpuacct:/docker/ebfaf125efecfe74d3a99b2d4ef584c3dc23fc290e834ff052ad87b16f5f0dbb
3:pids:/docker/ebfaf125efecfe74d3a99b2d4ef584c3dc23fc290e834ff052ad87b16f5f0dbb
2:memory:/docker/ebfaf125efecfe74d3a99b2d4ef584c3dc23fc290e834ff052ad87b16f5f0dbb
1:name=systemd:/docker/ebfaf125efecfe74d3a99b2d4ef584c3dc23fc290e834ff052ad87b16f5f0dbb
'''
        mocked_open = mock.mock_open(read_data=cgroup_contents)

        with mock.patch('__builtin__.open', mocked_open):
            assert_equal(uut.get_my_container_id(), 'ebfaf125efecfe74d3a99b2d4ef584c3dc23fc290e834ff052ad87b16f5f0dbb')

    def test_get_path_mount_no_container(self):
        '''Get path mount when not in docker'''
        cgroup_contents = '''12:devices:/user.slice
11:hugetlb:/
10:perf_event:/
9:net_cls,net_prio:/
8:cpuset:/
7:freezer:/
6:rdma:/
5:blkio:/user.slice
4:cpu,cpuacct:/user.slice
3:pids:/user.slice/user-1026.slice
2:memory:/user.slice
1:name=systemd:/user.slice/user-1026.slice/session-c1.scope
'''
        mocked_open = mock.mock_open(read_data=cgroup_contents)

        with mock.patch('__builtin__.open', mocked_open):
            test_path = '/tmp/test/path'
            host_path, mount_path, rel_path, mount_options = uut.get_path_mount(test_path)
            assert_equal(host_path, test_path)
            assert_equal(mount_path, test_path)
            assert_equal(rel_path, None)
            assert_equal(mount_options, None)

    def test_get_path_mount_volume_mount(self):
        '''Get path mount for a named volume'''
        
        container_id = container_inspect_data[0]['Id']
        def mocked_popen(popen_args, stdout = None, stderr = None):
            assert_equal(len(popen_args), 3)
            assert_equal(popen_args[0], 'docker')
            assert_equal(popen_args[1], 'inspect')
            assert_equal(popen_args[2], container_id)

            def mocked_communicate(self, stdin = None):
                return (self.stdout.read(), self.stderr.read())

            ret = type('popen_mock_obj', (), {})()
            ret.stdout = scuba.compat.StringIO(container_inspect_string)
            ret.stderr = scuba.compat.StringIO()
            ret.returncode = 0
            ret.communicate = MethodType(mocked_communicate, ret)
            return ret

        with mock.patch('scuba.dockerutil.Popen', mocked_popen):
            host_path, mount_path, rel_path, mount_options = uut.get_path_mount("/tester/workspace", container_id)
            assert_equal(host_path, "testvolume")
            assert_equal(mount_path, "/tester")
            assert_equal(rel_path, "workspace")
            assert_equal(mount_options, ["z"])

    def test_get_path_mount_bind_mount(self):
        '''Get path mount for a host volume'''
        
        container_id = container_inspect_data[0]['Id']
        def mocked_popen(popen_args, stdout = None, stderr = None):
            assert_equal(len(popen_args), 3)
            assert_equal(popen_args[0], 'docker')
            assert_equal(popen_args[1], 'inspect')
            assert_equal(popen_args[2], container_id)

            def mocked_communicate(self, stdin = None):
                return (self.stdout.read(), self.stderr.read())

            ret = type('popen_mock_obj', (), {})()
            ret.stdout = scuba.compat.StringIO(container_inspect_string)
            ret.stderr = scuba.compat.StringIO()
            ret.returncode = 0
            ret.communicate = MethodType(mocked_communicate, ret)
            return ret

        with mock.patch('scuba.dockerutil.Popen', mocked_popen):
            host_path, mount_path, rel_path, mount_options = uut.get_path_mount("/usermount/hostwork", container_id)
            assert_equal(host_path, "/home/user2")
            assert_equal(mount_path, "/usermount")
            assert_equal(rel_path, "hostwork")
            assert_equal(mount_options, [""])

