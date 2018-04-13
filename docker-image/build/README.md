# How to build an lrose image

## Prerequisits

All you need is the `Dockerfile` and maybe the `build.sh` scripts from [https://github.com/nsf-lrose/docker_scripts](https://github.com/nsf-lrose/docker_scripts)

In buid.sh, replace the **ORGANIZATION** and possibly **IMAGE** variables with your own.

## Build the image

./build.sh

When all set and done, you should have the image on your
system. Double check with

`docker images`

## Export the image

`docker export <image_ID> --output lrose-blaze.tgz`

## Copy it to another machine and import it

`docker import lrose-blaze.tgz`

## Building a custom image

The image generated with the given Dockerfile is a generic ubuntu image with just enough run-time libraries to support running lrose binaries.

If you wanted to add more packages, create additional users... you can either add instructions to the Dockerfile, or follow these steps

  * `docker run -it --name my_container /bin/bash`
  * Unless you specified a user (-u, --user) you should be root.
  * Add user(s), packages, ...
  * exit
  * `docker ps -a` to get your modified container ID
  * `docker commit <container_ID> mycustomimage`
  
`docker images` should now list your *mycustomimage*



