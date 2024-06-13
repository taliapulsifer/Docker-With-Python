import docker

#dockerClient = docker.DockerClient()

client = docker.from_env()

#This runs the command with the image and 
print(client.containers.run("alpine", ["echo", "hello", "world"]))

#Get and return a list of container. Also filters out the 
# containers built with a given image name
def getContainers(imageName):
    containersList = []
    containers = client.containers.list(all=True)
    for container in containers:
        if imageName in str(container.image):
            containersList.append(container)
    return containersList

#List all containers with no filtering
def allContainers():
    containersList = client.containers.list(all=True)
    return containersList

#Print all info for conatiners in list
def containersInfo(containerList):
    for container in containerList:
        print(f"ID: {container.id}, Name: {container.name}, Image: {container.image.tags}")

#Delete all containers
def removeAllContainers():
    containers = getContainers()
    for container in containers:
        try:
            container.stop()
            # Add exception handling here so that if the container refuses to 
            # stop we do not run into an error!!!
        except Exception as e:
            print("##############Error Stopping Container##############")
            print(container.name)
            print(e)
    client.prune(filter=None)

#Delete specific container
def removeContainer(containerName):
    containers = getContainers()
    for container in containers:
        if containerName in str(container.image):
            print("##############Deleting##############")
            print(container.name)
            try:
                client.stop(container)
                client.remove(container)
            except Exception as e:
                print("##############Error Deleting Container##############")
                print(container.name)
                print(e)

#Build Image and Start Containers (Start from existing image or create image if it does not exist)
def runContainer():
    #run(image, command=None, **kwargs)
    