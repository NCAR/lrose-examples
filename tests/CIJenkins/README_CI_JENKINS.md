
I’m thinking about using standard docker containers as clean starting points for testing installation and running of the lrose releases.

### Build centos-source container

make a docker base image with all the packages needed to build LROSE-Blaze.
Here is the command to build the container ...

```
% docker build —rm -t "centos-source:Dockerfile" -f centos-source.Dockerfile
% xhost +128.117.80.109:0
% docker run -ti --rm -e DISPLAY=128.117.80.109:0 -v /tmp/.X11-unix:/tmp/.X11-unix:rw centos:7
[root@1fe1ed5e89bb /]# history
    1  yum install -y xorg-x11-server-Xorg xorg-x11-xauth xorg-x11-apps
    2  xclock&
    3  history
[1]+  Done                    xclock
```

and here is the [Dockerfile](Dockerfile)

## Continuous integration and deployment [DevOps] with docker containers…

https://www.digitalocean.com/community/tutorials/how-to-configure-a-continuous-integration-testing-environment-with-docker-and-docker-compose-on-ubuntu-14-04

### Some background info on Jenkins ...

```
Jenkinsfile (Declarative Pipeline)
pipeline {
    // agent any
    agent {
        docker { image 'node:7-alpine' }  <<---- Note! an agent is a docker container; the stages are run in this container
    }
    stages {
        stage('Build') {
            steps {
                //  sh 'echo "building lrose-blaze"'
            }
        }
        stage('Test') {
            steps {
                //
            }
        }
        stage('Deploy') {   // make an rpm and install it on a clean image
            steps {
                //
            }
        }
    }
    post {
        always {
            echo 'This will always run'
        }
        success {
            echo 'This will run only if successful'
        }
        failure {
            echo 'This will run only if failed'
        }
        unstable {
            echo 'This will run only if the run was marked as unstable'
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, if the Pipeline was previously failing but is now successful'
        }
    }
}
```

run jenkins as a container in Docker ...
The recommended docker image is jenkinsci/blueocean

```
docker run \
  --rm \
  -u root \
  -p 8080:8080 \
  -v jenkins-data:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$HOME":/home \

  jenkinsci/blueocean
```
I modified the above command to ...
```
docker run \
  --rm
  --name jenkins-blueocean \
  -u root \
  -p 8083:8080 \
  -v jenkins-data:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkinsci/blueocean
```

command-line interface to jenkins ...
build ... console ...

Try running Jenkins as a container in Docker ... DONE.

Now, try Jenkins performing an lrose build inside a container.

#### docker

Execute the Pipeline, or stage, with the given container which will be dynamically provisioned on a node pre-configured to accept Docker-based Pipelines, or on a node matching the optionally defined label parameter. docker also optionally accepts an args parameter which may contain arguments to pass directly to a docker run invocation, and an alwaysPull option, which will force a docker pull even if the image name is already present. For example:

```
 agent { docker 'maven:3-alpine' } 
```
or

```
agent {
    docker {
        image 'maven:3-alpine'
        label 'my-defined-label'
        args  '-v /tmp:/tmp'
    }
}
```

#### dockerfile

Execute the Pipeline, or stage, with a container built from a Dockerfile contained in the source repository. In order to use this option, the Jenkinsfile must be loaded from either a Multibranch Pipeline, or a "Pipeline from SCM." Conventionally this is the Dockerfile in the root of the source repository: 
```
agent { dockerfile true }. 
```
If building a Dockerfile in another directory, use the dir option: 
```
agent { dockerfile { dir 'someSubDir' } }
```
If your Dockerfile has another name, you can specify the file name with the filename option. You can pass additional arguments to the docker build ... command with the additionalBuildArgs option, like 
``` agent { dockerfile { additionalBuildArgs '--build-arg foo=bar' } }. ```
For example, a repository with the file build/Dockerfile.build, expecting a build argument version:

```
agent {
    // Equivalent to "docker build -f Dockerfile.build --build-arg version=1.0.2 ./build/
    dockerfile {
        filename 'Dockerfile.build'
        dir 'build'
        label 'my-defined-label'
        additionalBuildArgs  '--build-arg version=1.0.2'
    }
}
```

## STUCK HERE: The problem is jenkins user doesn't have permission to contact the docker daemon. 

```
docker exec -it 0a8499c63e904274fca49b7c42112e5418da8ae030e2a42e6d0d4d67591170ce  bash

```
## moving on in a different direction 

build docker image for continuous integration, on Mac in ~/CI/test_lrose_blaze/Jenkins:

```
docker build --rm -t "centos-jenkins-base" -f centos-jenkins-base.Dockerfile .
```

centos-jenkins-base.Dockerfile:
```
#
# start with an image that contains all the packages needed to 
# build lrose 
#
FROM centos-source:Dockerfile

ADD . /tmp/bj
 
RUN yum -y install git
RUN yum -y install libtool

# These will be run by Jenkins script ...
# RUN  cd /tmp/bj; tar xvfz lrose-blaze-20180516.src.tgz  
# The distribution will be unpacked into a subdirectory:

# RUN /tmp/bj/lrose-blaze-20180516.src/build/checkout_and_build_auto.py --package lrose-blaze --prefix /usr/local/lrose --clean
```

Jenkins pipeline script 
```
pipeline {
  
    agent {
        //docker { image 'nsflrose/lrose-blaze:latest' }
        //docker { image 'centos-source:Dockerfile' }
        docker { image 'centos-jenkins-base:latest' }
    }
    stages {
        stage('Fetch and Build') {
            steps {
                sh 'cd /tmp/bj; tar xvfz lrose-blaze-20180516.src.tgz'

                // The distribution will be unpacked into a subdirectory:

                sh '/tmp/bj/lrose-blaze-20180516.src/build/checkout_and_build_auto.py --package lrose-blaze --prefix /usr/local/lrose --clean'
            }
        }
        
        stage('Test') {
            steps {
                sh 'RadxPrint -h'
            }
        }
    }
    
//agent {
//      dockerfile {
//          filename 'centos-source.Dockerfile'
//          dir 'tests/CIJenkins'
//          label 'scooby-doo'
//          additionalBuildArgs ''
//      }
//}

//pipeline {
//    agent {
//        docker {
//            image 'centos-source:Dockerfile'
//        }
//    }

/*------  
    agent none  
    
    stages {
        stage('Test') {
            agent {
                docker { image 'centos-source:Dockerfile' }
            }
            steps {
                sh 'echo "Good Evening"'
                sh 'pwd'
                sh 'ls'
            }
        }
    }    
    // -----------
    */
}

```
works pretty well ... stuck here in testing ...
```
[build lrose-blaze] Running shell script
+ ls -lrt /usr/local/lrose/bin
total 5116
-rwxr-xr-x 1 root root  242240 Aug  8 16:52 h5diff
-rwxr-xr-x 1 root root  174080 Aug  8 16:52 h5ls
-rwxr-xr-x 1 root root  237928 Aug  8 16:52 h5dump
-rwxr-xr-x 1 root root   18864 Aug  8 16:52 h5debug
-rwxr-xr-x 1 root root   18376 Aug  8 16:52 h5repart
-rwxr-xr-x 1 root root  141456 Aug  8 16:52 h5mkgrp
-rwxr-xr-x 1 root root    6109 Aug  8 16:52 h5redeploy
-rwxr-xr-x 1 root root   13322 Aug  8 16:52 h5cc
-rwxr-xr-x 1 root root  196296 Aug  8 16:52 h5import
-rwxr-xr-x 1 root root  224528 Aug  8 16:52 h5repack
-rwxr-xr-x 1 root root  146160 Aug  8 16:52 h5jam
-rwxr-xr-x 1 root root  141912 Aug  8 16:52 h5unjam
-rwxr-xr-x 1 root root  145808 Aug  8 16:52 h5copy
-rwxr-xr-x 1 root root  156144 Aug  8 16:52 h5stat
-rwxr-xr-x 1 root root  183696 Aug  8 16:52 h5perf_serial
-rwxr-xr-x 1 root root   13113 Aug  8 16:52 h5c++
-rwxr-xr-x 1 root root   12779 Aug  8 16:52 h5fc
-rwxr-xr-x 1 root root  151768 Aug  8 16:52 gif2h5
-rwxr-xr-x 1 root root  142336 Aug  8 16:52 h52gif
-rwxr-xr-x 1 root root   19792 Aug  8 16:52 udunits2
-rwxr-xr-x 1 root root  101344 Aug  8 16:53 ncgen3
-rwxr-xr-x 1 root root  270840 Aug  8 16:53 ncgen
-rwxr-xr-x 1 root root  110184 Aug  8 16:53 ncdump
-rwxr-xr-x 1 root root   62216 Aug  8 16:53 nccopy
-rwxr-xr-x 1 root root    6222 Aug  8 16:53 nc-config
-rwxr-xr-x 1 root root    3065 Aug  8 16:53 nf-config
-rwxr-xr-x 1 root root    2735 Aug  8 16:54 ncxx4-config
-rwxr-xr-x 1 root root  614944 Aug  8 17:00 Radx2Grid
-rwxr-xr-x 1 root root  236952 Aug  8 17:00 RadxConvert
-rwxr-xr-x 1 root root  101400 Aug  8 17:00 RadxPrint
-rwxr-xr-x 1 root root 1112496 Aug  8 17:00 HawkEye
-rwxr-xr-x 1 root root   88608 Aug  8 17:00 tdrp_gen
-rwxr-xr-x 1 root root   30992 Aug  8 17:00 tdrp_test
-rwxr-xr-x 1 root root   43496 Aug  8 17:00 TdrpTest
[Pipeline] sh
[build lrose-blaze] Running shell script
+ /usr/local/lrose/bin/RadxPrint -h
/usr/local/lrose/bin/RadxPrint: error while loading shared libraries: libdsdata.so.0: cannot open shared object file: No such file or directory
[Pipeline] }
[Pipeline] // stage
[Pipeline] }
$ docker stop --time=1 05e49ef7b35a8bdde3cb7626a9375265767125c28476e96fb8b93ab1b51ad614
$ docker rm -f 05e49ef7b35a8bdde3cb7626a9375265767125c28476e96fb8b93ab1b51ad614
[Pipeline] // withDockerContainer
[Pipeline] }
[Pipeline] // node
[Pipeline] End of Pipeline
ERROR: script returned exit code 127
Finished: FAILURE
```
