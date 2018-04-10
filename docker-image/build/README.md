# How to build an lrose image

## Prerequisits

All you need is the `Dockerfile` in this directory, and
checkout_and_build_auto.py[https://github.com/NCAR/lrose-core/blob/master/build/checkout_and_build_auto.py] from the lrose-core/build directory.

## Build the image

Copy both to a build directory, for example `~/build`, `cd` to it,
then

`docker build -t lrose-blaze .`

When all set and done, you should have the image on your
system. Double check with

`docker images`

## Export the image

`docker export --output lrose-blaze.tgz`

## Copy it to another machine and import it

`docker import lrose-blaze.tgz`

## TODO

The generated image is quite large. Larger than one where I just
installed the needed runtime libraries, and untarred an lrose
distribution created in another image. I need to investigate the
difference.




