import config
import numpy as np
from mayavi import mlab


class Map:
    def __init__(self,x,y,z):
        self.slow_cache = {}
        self.slow_cache['size'] = (x+2,y+2,z)
        self.slow_cache['map'] = np.random.randint(0,2,size=(x+2,y+2,z))
        self.centralization()
        self.deposition()
        for i in range(4):
          self.flow()
          self.deposition()
        self.slow_cache['map'] = self.slow_cache['map'][1:x+1,1:y+1,:]
        self.slow_cache['size'] = (x,y,z)
        self.slow_cache['map'] = np.concatenate((np.ones((x,y,z),self.slow_cache['map'])),axis=2)
        mlab.points3d(self.slow_cache['map'],mode="cube",colormap='copper', scale_factor=1)
        mlab.show()
    def centralization(self):
        for k in range(self.slow_cache['size'][2]):
            for i in range(self.slow_cache['size'][0]):
                for j in range(self.slow_cache['size'][1]):
                    if (-np.log((np.abs(i-self.slow_cache['size'][0]/2)**2+np.abs(j-self.slow_cache['size'][0]/2)**2)**0.5+1) +np.log((self.slow_cache['size'][0]**2+(self.slow_cache['size'][1]**2))**0.5))*4/np.log((self.slow_cache['size'][0]**2+(self.slow_cache['size'][1]**2))) < np.random.rand(1):
                        self.slow_cache['map'][i,j,k] = 0

    def flow(self):
        for k in range(self.slow_cache['size'][2]):
            for i in range(1,self.slow_cache['size'][0]-1):
                for j in range(1,self.slow_cache['size'][1]-1):
                    if not ((np.array([[0,1,0],[1,1,1],[0,1,0]])*self.slow_cache['map'][i-1:i+2,j-1:j+2,k] == np.array([[0,1,0],[1,1,1],[0,1,0]])).all() or (np.array([[0,1,0],[1,1,1],[0,1,0]])*self.slow_cache['map'][i-1:i+2,j-1:j+2,k] == np.array([[0,1,0],[1,1,0],[0,1,0]])).all() or (np.array([[0,1,0],[1,1,1],[0,1,0]])*self.slow_cache['map'][i-1:i+2,j-1:j+2,k] == np.array([[0,1,0],[0,1,1],[0,1,0]])).all() or (np.array([[0,1,0],[1,1,1],[0,1,0]])*self.slow_cache['map'][i-1:i+2,j-1:j+2,k] == np.array([[0,0,0],[1,1,1],[0,1,0]])).all() or (np.array([[0,1,0],[1,1,1],[0,1,0]])*self.slow_cache['map'][i-1:i+2,j-1:j+2,k] == np.array([[0,1,0],[1,1,1],[0,0,0]])).all() ):
                        if np.random.random(1) < 0.9:
                            self.slow_cache['map'][i,j,k] = 0

    def deposition(self):
        for k in range(self.slow_cache['size'][2]):
            print(k)
            for i in range(self.slow_cache['size'][0]):
                for j in range(self.slow_cache['size'][1]):
                    temp = k
                    while True:
                            if temp-1 >= 0 and self.slow_cache['map'][i,j,temp] > 0:
                                if self.slow_cache['map'][i,j,temp-1] == 0:
                                    self.slow_cache['map'][i,j,temp-1] = 1
                                    self.slow_cache['map'][i,j,temp] = 0
                                    temp -= 1
                                else:
                                    break
                            else:
                                break




if __name__ == "__main__":
    m = Map(128,128,64)


