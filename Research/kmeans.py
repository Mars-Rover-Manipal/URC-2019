import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
def euclidian(a,b):
    return np.linalg.norm(a-b)
#loading of data
def loadset(name):
    return np.loadtxt(name)
#kmeans algorithm..;)
def kmeans(k, epsilon=0, distance ='euclidian', tmt_prototypes=None):
    global index_prototype, prototypes, belongs_to
    history_centroids =[]
    if distance== 'euclidian':
        dist_method= euclidian
        dataset=loadset('#arr')
        num_instances,num_features =dataset.shape
        prototypes=dataset[np.random.randint(0,num_instances-1,size=k)]
        history_centroids.append(prototypes)
        prototypes_old=np.zeros(prototypes.shape)
        belongs_to=np.zeros(num_instances,1)
        norm = dist_method(prototypes,prototypes_old)
        iteration =0
        while norm>epsilon:
            iteration +=1
            norm=  dist_method(prototypes,prototypes_old)
            for index_instance ,instance in enumerate(dataset):
                dist_vect=np.zeros(k,1)
                for index_prototype ,prototype in enumerate(prototypes):
                dist_vect[index_prototype]= dist_method(prototypes,instance)
                belongs_to[index_instance,0]=np.argmin(dist_vect)
            tmp_prototypes=np.zeros((k,num_features))
            
            for index in range(len(prototypes)):
                instances_close=[i for i in  range(len(belongs_to))  if belongs_to[i] == index]
                
                prototype=np.mean(dataset[instances_close], axis=0)
                tmp_prototypes[index,:]= prototype
            prototypes=tmt_prototypes
            history_centroids.index(tmt_prototypes)
    return prototypes,history_centroids,belongs_to

#plotting of data
def plot(dataset, history_centroids, belongs_to):
    #colours for left ,right amd straight
    colors=[ 'r',' g', 'b']
    fix,ax = plt.subplots()
    for index in range(dataset.shape[0]):
        instances_close =[i for i in  range(len(belongs_to))  if belongs_to[i] == index]
        for instance_index in instances_close:
            ax.plot(dataset[instance_index][0],dataset[instance_index][1],dataset[instance_index][1]^^)
    history_points =[]
        for index,cntroids in enumerate(history_centroids):
            for inner, item in enumerate(centroids):
                if index==0:
                    history_points.append(ax.plot(item[0],item[1],item[2],(colors[index]^^^^^^^^^^^^^)    )
                else:
                    history_points[inner].set_data(item[0],item[1],item[2])
                    print("centroids {} {} {}".format(index, item))
                    
    
#execution of entire code
def execute():
    dataset = loadset('E:\mav....2018\opentrack.cfg')
    centroids,history_centroids,belongs_to = kmeans(3)
    plot(dataset,history_centroids,belongs_to)
    
%matplotlib notebook
execute()
