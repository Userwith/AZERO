import config
import numpy as np
from mayavi import mlab
from perlin_noise import PerlinNoise
class Map:
    def __init__(self,render_radius,z,octaves,seed,sea_level):
        self.slow_cache = {}
        self.slow_cache['render_radius'] = render_radius
        self.slow_cache['z'] = z
        self.slow_cache['octaves'] = octaves
        self.slow_cache['seed'] = seed
        self.slow_cache['sea_level'] = sea_level
        self.slow_cache['noise1'] = PerlinNoise(octaves=octaves,seed=seed)
        self.slow_cache['noise2'] = PerlinNoise(octaves=octaves,seed=2*seed)
        self.slow_cache['map_3d'] = np.zeros((2*render_radius,2*render_radius,z))
        self.slow_cache['curr_location'] = np.zeros(2)
        for i in range(2*render_radius):
            for j in range(2*render_radius):
                high = int(0.5*(self.slow_cache['noise1']([(-render_radius+i)/128,(-render_radius+j)/128])+1) * z * 0.5*(self.slow_cache['noise2']([(-render_radius+i)/128,(-render_radius+j)/128])+1))
                self.slow_cache['map_3d'][i, j, :high] = np.ones(high)
                if high < int(sea_level):
                    self.slow_cache['map_3d'][i, j, high:sea_level] = 2 * np.ones(sea_level - high)

    def update(self,camera_location):
        bios = (camera_location-self.slow_cache['curr_location']).astype(int)
        abs_bios = np.maximum(bios,-bios)
        bios_xmap = np.zeros([abs_bios[0],2*self.slow_cache['render_radius'],self.slow_cache['z']])
        bios_ymap = np.zeros([2*self.slow_cache['render_radius']-abs_bios[0],abs_bios[1],self.slow_cache['z']])
        for i in range(2 * self.slow_cache['render_radius']-abs_bios[0]):
            for j in range(abs_bios[1]):
                if bios[0]>0:
                    high = int(0.5*(self.slow_cache['noise1']([(camera_location[0]-self.slow_cache['render_radius']+i)/128,(camera_location[1]+j)/128])+1) * self.slow_cache['z'] * 0.5*(self.slow_cache['noise2']([(camera_location[0]-self.slow_cache['render_radius']+i)/128,(camera_location[1]+j)/128])+1))
                else:
                    high = int(0.5*(self.slow_cache['noise1']([(camera_location[0]+self.slow_cache['render_radius']-i)/128,(camera_location[1]+j)/128])+1) * self.slow_cache['z'] * 0.5*(self.slow_cache['noise2']([(camera_location[0]-self.slow_cache['render_radius']+i)/128,(camera_location[1]+j)/128])+1))

                bios_ymap[i,j,:high] = np.ones(high)
                if high < int(self.slow_cache['sea_level'] ):
                    bios_ymap[i, j, high:self.slow_cache['sea_level'] ] = 2 * np.ones(self.slow_cache['sea_level']  - high)

        for i in range(abs_bios[0]):
            for j in range(2 * self.slow_cache['render_radius']):
                if bios[0] < 0:
                    high = int(0.5 * (self.slow_cache['noise1'](
                    [(self.slow_cache['curr_location'][0] + bios[0] + i) / 128,
                     (self.slow_cache['curr_location'][1] + bios[1] - self.slow_cache['render_radius'] + j) / 128]) + 1) * self.slow_cache['z'] * 0.5 * (self.slow_cache['noise2'](
                    [(self.slow_cache['curr_location'][0] + bios[0] + i) / 128,
                     (self.slow_cache['curr_location'][1] + bios[1] - self.slow_cache['render_radius'] + j) / 128]) + 1))
                else:
                    high = int(0.5 * (self.slow_cache['noise1'](
                        [(self.slow_cache['curr_location'][0] + bios[0] - i) / 128,
                         (self.slow_cache['curr_location'][1] + bios[1] - self.slow_cache['render_radius'] + j) / 128]) + 1) * self.slow_cache[
                                   'z'] * 0.5 * (self.slow_cache['noise2'](
                        [(self.slow_cache['curr_location'][0] + bios[0] - i) / 128,
                         (self.slow_cache['curr_location'][1] + bios[1] - self.slow_cache['render_radius'] + j) / 128]) + 1))
                bios_xmap[i, j, :high] = np.ones(high)
                if high < int(self.slow_cache['sea_level']):
                    bios_xmap[i, j, high:self.slow_cache['sea_level']] = 2 * np.ones(
                        self.slow_cache['sea_level'] - high)
        if bios[0] > 0:
            self.slow_cache['map_3d'] = self.slow_cache['map_3d'][bios[0]:,:]
        elif bios[0] < 0:
            self.slow_cache['map_3d'] = self.slow_cache['map_3d'][:bios[0],:]
        if bios[1] > 0:
            self.slow_cache['map_3d'] = self.slow_cache['map_3d'][:,bios[1]:]
        elif bios[1] < 0:
            self.slow_cache['map_3d'] = self.slow_cache['map_3d'][:,:bios[1]]

        if bios_ymap.shape[0] > 0:
            if bios[1] > 0:
                self.slow_cache['map_3d'] = np.concatenate((self.slow_cache['map_3d'],bios_ymap), axis=1)
            else:
                self.slow_cache['map_3d'] = np.concatenate((bios_ymap,self.slow_cache['map_3d']), axis=1)

        if bios_xmap.shape[0] > 0 :
            if bios[0]>0:
                self.slow_cache['map_3d'] = np.concatenate((self.slow_cache['map_3d'],bios_xmap),axis=0)
            else:
                self.slow_cache['map_3d'] = np.concatenate((bios_xmap,self.slow_cache['map_3d']),axis=0)








if __name__ == "__main__":
    m = Map(32,128,4,100,32)
    m.update(np.array([-10,0]))
    mlab.points3d(m.slow_cache['map_3d'], mode='cube', colormap='copper', scale_factor=.9)
    mlab.show()
    print(m.slow_cache['map_3d'].shape)

