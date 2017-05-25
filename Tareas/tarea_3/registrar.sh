IMAGE_VERSION="0.1"
IMAGES="python dpa-flask"

for IMAGE in ${IMAGES} ; do
	echo $IMAGE
    docker build --tag tarea_3/${IMAGE}:${IMAGE_VERSION} ${IMAGE}
done