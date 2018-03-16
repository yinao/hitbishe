# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 10:31:40 2018

@author: zhouying
"""
import numpy as np
def consin(vec1,vec2):
    import numpy as np
    cons = np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))
    return cons

def gaussian(dist,a=1,b=0,c=0.5):
    import math
    return a*math.e**(-(dist-b)**2/(2*c**2))

#def 

def dis(dist,metrix):
    a = 1/metrix
    return (1/dist)/sum(a)

def generalized_ir(arg):
    data,label = arg
#    import numpy as np
    from sklearn.neighbors import NearestNeighbors
#    
    nbrs = NearestNeighbors(n_neighbors=6, algorithm="auto").fit(data)
    _,indices = nbrs.kneighbors(data)
    
    positvie =1
    negative = -1
    
    nn = indices[:,1:]
    Tplas = 0.
    Tminas=0.
    for i in range(label.shape[0]):
        if label[i] == positvie :
            for value in label[nn[i]]:
                if value == positvie:
                    Tplas+=1
        elif label[i]==negative:
            for value in label[nn[i]]:
                if value == negative:
                    Tminas+=1
            
            
    Tplas/=label[label==positvie].shape[0]*nn.shape[1]
    Tminas/=label[label==negative].shape[0]*nn.shape[1]
    gr = Tminas-Tplas
    print("the generalized imbalance rate is %.3f"%(gr))
    return Tminas-Tplas,(Tminas*Tplas)**0.5

def weighted_generalized_ir(arg):
    data,label = arg
#    import numpy as np
    from sklearn.neighbors import NearestNeighbors
    nbrs = NearestNeighbors(n_neighbors=6, algorithm="auto").fit(data)
    _,indices = nbrs.kneighbors(data)
    
    positvie =1
    negative = 0
    
    nn = indices[:,1:]
    Tplas = 0.
    Tminas=0.
    for i in range(label.shape[0]):
        weight = 1
        if label[i] == positvie :
            for value in label[nn[i]]:
                if value == positvie:
                    Tplas+=1*weight
                weight -=0.2
        elif label[i]==negative:
            for value in label[nn[i]]:
                if value == negative:
                    Tminas+=1*weight
                weight -=0.2
    Tplas/=label[label==positvie].shape[0]*nn.shape[1]
    Tminas/=label[label==negative].shape[0]*nn.shape[1]
    gr = Tminas-Tplas
    print("the weighted generalized imbalance rate is %.3f"%(gr))
    return Tminas-Tplas,(Tminas*Tplas)**0.5



'''
###############################################################################
对比状态中的各类GIR计算
###############################################################################
'''

'''基于consin值的对GIR的平均值进行加权计算'''
def weighted_consin_generalized_ir(arg):
    data,label = arg
    import numpy as np
    k = 6
    from sklearn.neighbors import NearestNeighbors
#    
    nbrs = NearestNeighbors(n_neighbors=k, algorithm="auto").fit(data)
    _,indices = nbrs.kneighbors(data)
    
    positvie =1
    negative = 0
    
    nn = indices[:,1:]
    Tplas = 0.
    Tminas=0.
    total = np.zeros(label.shape[0])
    for i in range(label.shape[0]):
        get = 1
        if label[i] == positvie :
            for value,index in zip(label[nn[i]],data[nn[i]]):
                if value == positvie:
                    wei = np.abs(consin(data[i],index))
                    if np.isnan(wei):
                        wei = 1
                    Tplas+=1*wei*get
                    total[i]+=1*wei*get
                get-=0.2
        elif label[i]==negative:
            for value,index in zip(label[nn[i]],data[nn[i]]):
                if value == negative:
                    wei = np.abs(consin(data[i],index))
                    if np.isnan(wei):
                        wei=1
                    Tminas+=1*wei*get
                    total[i]+=1*wei*get
                get-=0.2
            
            
    Tplas/=label[label==positvie].shape[0]*nn.shape[1]
    Tminas/=label[label==negative].shape[0]*nn.shape[1]
    total /=(k-1)
    gr = Tminas-Tplas
    return gr

'''基于高斯函数的欧式距离加权，计算GIR的平均值'''
def weighted_gaussian_generalized_ir(arg):
    data,label = arg
    import numpy as np
    k = 6
    from sklearn.neighbors import NearestNeighbors
#    
    nbrs = NearestNeighbors(n_neighbors=k, algorithm="auto").fit(data)
    dist,indices = nbrs.kneighbors(data)
    
    positvie =1
    negative = 0
    
    nn = indices[:,1:]
    dist = dist[:,1:]
    c1 = np.mean(dist[label==1])
    c0 = np.mean(dist[label==0])
    Tplas = 0.
    Tminas=0.
    total = np.zeros(label.shape[0])
    for i in range(label.shape[0]):
        get = 1
        if label[i] == positvie :
            for value,index in zip(label[nn[i]],dist[i]):
                if value == positvie:
                    wei = gaussian(index,a=1,b=0,c=c1)#dis(index,dist[i])#
                    if np.isnan(wei):
                        wei = 1
                    Tplas+=1*wei*get
                    total[i]+=1*wei*get
                get-=0.2
        elif label[i]==negative:
            for value,index in zip(label[nn[i]],dist[i]):
                if value == negative:
                    wei = gaussian(index,a=1,b=0,c=c0)#dis(index,dist[i])
                    if np.isnan(wei):
                        wei=1
                    Tminas+=1*wei*get
                    total[i]+=1*wei*get
                get-=0.2
    Tplas/=label[label==positvie].shape[0]*nn.shape[1]
    Tminas/=label[label==negative].shape[0]*nn.shape[1]
    total /=(k-1)
    gr = Tminas-Tplas
    print("the generalized gaussian imbalance rate is %.3f"%(gr))
    return (Tminas*Tplas)**0.5

'''基于距离倒数归一化的加权方法'''
def weighted_normalize_generalized_ir(arg):
    data,label = arg
    import numpy as np
    k = 6
    from sklearn.neighbors import NearestNeighbors
#    
    nbrs = NearestNeighbors(n_neighbors=k, algorithm="auto").fit(data)
    dist,indices = nbrs.kneighbors(data)
    
    positvie =1
    negative = 0
    
    nn = indices[:,1:]
    dist = dist[:,1:]
    Tplas = 0.
    Tminas=0.
    total = np.zeros(label.shape[0])
    for i in range(label.shape[0]):
        get = 1
        if label[i] == positvie :
            for value,index in zip(label[nn[i]],dist[i]):
                if value == positvie:
                    wei = dis(index,dist[i])#
                    if np.isnan(wei):
                        wei = 1
                    Tplas+=1*wei*get
                    total[i]+=1*wei*get
                get-=0.2
        elif label[i]==negative:
            for value,index in zip(label[nn[i]],dist[i]):
                if value == negative:
                    wei = dis(index,dist[i])
                    if np.isnan(wei):
                        wei=1
                    Tminas+=1*wei*get
                    total[i]+=1*wei*get
                get-=0.2
    Tplas/=label[label==positvie].shape[0]*nn.shape[1]
    Tminas/=label[label==negative].shape[0]*nn.shape[1]
    total /=(k-1)
    gr = Tminas-Tplas
    print("the generalized normalized imbalance rate is %.3f"%(gr))
    return gr






























#general_ir returns the point-wise general imbalance ratio and the total genenral-ir
def general_ir(arg,k=6):
    data,label = arg
    import numpy as np
    from sklearn.neighbors import NearestNeighbors
#    
    nbrs = NearestNeighbors(n_neighbors=k, algorithm="auto").fit(data)
    _,indices = nbrs.kneighbors(data)
    
    positvie =1
    negative = 0
    
    nn = indices[:,1:]
    Tplas = 0.
    Tminas=0.
    total = np.zeros(label.shape[0])
    for i in range(label.shape[0]):
        if label[i] == positvie :
            for value in label[nn[i]]:
                if value == positvie:
                    Tplas+=1
                    total[i]+=1
        elif label[i]==negative:
            for value in label[nn[i]]:
                if value == negative:
                    Tminas+=1
                    total[i]+=1
            
            
    Tplas/=label[label==positvie].shape[0]*nn.shape[1]
    Tminas/=label[label==negative].shape[0]*nn.shape[1]
    total /=(k-1)
    gr = Tminas-Tplas
#    print("the generalized imbalance rate is %.3f"%(gr))
    return Tplas,Tminas,total

def weighted_general_ir(arg,k=6):
    data,label = arg
    import numpy as np
    from sklearn.neighbors import NearestNeighbors
#    
    nbrs = NearestNeighbors(n_neighbors=k, algorithm="auto").fit(data)
    _,indices = nbrs.kneighbors(data)
    
    positvie =1
    negative = 0
    
    nn = indices[:,1:]
    Tplas = 0.
    Tminas=0.
    total = np.zeros(label.shape[0])
    for i in range(label.shape[0]):
        wei = 1
        if label[i] == positvie :
            for value in label[nn[i]]:
                if value == positvie:
                    Tplas+=1*wei
                    total[i]+=1*wei
                wei -=0.2
        elif label[i]==negative:
            for value in label[nn[i]]:
                if value == negative:
                    Tminas+=1*wei
                    total[i]+=1*wei
                wei-=0.2
            
            
    Tplas/=label[label==positvie].shape[0]*nn.shape[1]
    Tminas/=label[label==negative].shape[0]*nn.shape[1]
    total /=(k-1)
    gr = Tminas-Tplas
#    print("the generalized imbalance rate is %.3f"%(gr))
    return Tplas,Tminas,total

def boundary_gir(arg,k=6):
    data,label = arg
    import numpy as np
    from sklearn.neighbors import NearestNeighbors
#    
    nbrs = NearestNeighbors(n_neighbors=k, algorithm="auto").fit(data)
    _,indices = nbrs.kneighbors(data)
    
    positvie =1
    negative = 0
    
    nn = indices[:,1:]
    Tplas = 0.
    Tminas=0.
    total = np.zeros(label.shape[0])
    for i in range(label.shape[0]):
        wei = 1
        if label[i] == positvie :
            for value in label[nn[i]]:
                if value == positvie:
                    Tplas+=1*wei
                    total[i]+=1*wei
                wei -=0.2
        elif label[i]==negative:
            for value in label[nn[i]]:
                if value == negative:
                    Tminas+=1*wei
                    total[i]+=1*wei
                wei-=0.2
            
            
    Tplas/=label[label==positvie].shape[0]*nn.shape[1]
    Tminas/=label[label==negative].shape[0]*nn.shape[1]
    total /=(k-1)    
    gr = Tminas-Tplas
    from untitled0 import boundary
#    print("the generalized imbalance rate is %.3f"%(gr))
    reduce = boundary([data,label])
    total[reduce]-=0.1
    return Tplas,Tminas,total

def consin_generalized_ir(arg):
    data,label = arg
    import numpy as np
    k = 6
    from sklearn.neighbors import NearestNeighbors
#    
    nbrs = NearestNeighbors(n_neighbors=k, algorithm="auto").fit(data)
    _,indices = nbrs.kneighbors(data)
    
    positvie =1
    negative = 0
    
    nn = indices[:,1:]
    Tplas = 0.
    Tminas=0.
    total = np.zeros(label.shape[0])
    for i in range(label.shape[0]):
        get = 1
        if label[i] == positvie :
            for value,index in zip(label[nn[i]],data[nn[i]]):
                if value == positvie:
                    wei = np.abs(consin(data[i],index))
                    if np.isnan(wei):
                        wei = 1
                    Tplas+=1*wei*get
                    total[i]+=1*wei*get
                get-=0.2
        elif label[i]==negative:
            for value,index in zip(label[nn[i]],data[nn[i]]):
                if value == negative:
                    wei = np.abs(consin(data[i],index))
                    if np.isnan(wei):
                        wei=1
                    Tminas+=1*wei*get
                    total[i]+=1*wei*get
                get-=0.2
            
            
    Tplas/=label[label==positvie].shape[0]*nn.shape[1]
    Tminas/=label[label==negative].shape[0]*nn.shape[1]
    total /=(k-1)
    gr = Tminas-Tplas
#    print("the generalized consin imbalance rate is %.3f"%(gr))
    return Tplas,Tminas,total