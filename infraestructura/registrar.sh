IMAGE_VERSION="0.1"
DOCKER_REGISTRY="localhost:5000"
IMAGES="python luigi-server luigi-worker python-selenium compranet/download-declaranet"


for IMAGE in ${IMAGES} ; do
	echo $IMAGE
    docker build --tag ${DOCKER_REGISTRY}/dpa/${IMAGE}:${IMAGE_VERSION} --tag dpa/${IMAGE}:${IMAGE_VERSION} ${IMAGE}
    docker push ${DOCKER_REGISTRY}/dpa/${IMAGE}:${IMAGE_VERSION}
done
