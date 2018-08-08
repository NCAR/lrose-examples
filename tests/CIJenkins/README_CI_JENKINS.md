
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
