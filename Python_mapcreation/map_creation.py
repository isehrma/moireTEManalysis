import numpy as np
import matplotlib.pyplot as plt
import cv2

class Photo:
    def __init__(self, name):
        self.name = name
        # names should be in the format: nameoffile_angle_radius.jpg
        self.photo = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
        self.photo_matrix = self.photo 
        filter(None, self.photo_matrix)
        elements_of_name = name.split('_')
        self.angle = int(elements_of_name[1])
        self.radius = int(elements_of_name[2])
        self.average = self.mean()
        self.std_ = self.std()
    
    def show(self):
        plt.imshow(self.photo_matrix, cmap='gray')
        plt.show()

    # we will need to adjust contrast and brightness of the photo later
    def change_brightness_and_contrast(self, alpha, beta):
        self.photo = cv2.convertScaleAbs(self.photo, alpha, beta)
        self.photo_matrix = np.array(self.photo)
    
    # function which will turn the matrix of n=(0,225) values 
    # into a matrix of (0,1) values
    def binarize(self,bin_threshhold):
        self.photo_matrix = np.where(self.photo_matrix > bin_threshhold, 1, 0)
        return self.photo_matrix
    
    def save(self):
        cv2.imwrite(self.name, self.photo_matrix)
        return self.photo_matrix
    
    def xsize(self):
        return self.xsize
    
    def ysize(self):
        return self.ysize
    
    def read(self):
        print (self.photo_matrix)
        print (self.angle)
        print (self.radius)
    
    def average(self):
        return self.average

    def std(self):
        return self.std_
  
        
class Pixel:
    def __init__(self,x,y, matrix_of_angles, matrix_of_radii):
        self.x = x
        self.y = y
        self.amatrix = matrix_of_radii
        self.rmatrix = matrix_of_angles
    

    def average(self): # this function will return the average of 
                       #the angles and radiuses of the pixel
        n = 0
        m = 0
        w = 0
        z = 0

        for i in range(len(self.amatrix)):
            if self.amatrix[i] == 0:
                n += i
                w += 1

        for i in range(len(self.rmatrix)):
            if self.rmatrix[i] == 0:
                m += i
                z += 1

        if w == 0:
            n = angle_n0
        else: 
            i = n/w
            a_i = (end_angle - beginning_angle)/number_of_angles*i +beginning_angle
            a_i1 = (end_angle - beginning_angle)/number_of_angles*(i+1) +beginning_angle
            n = (a_i1 + a_i)/2

        
        if z == 0:
            m = radius_m0
        else: 
            j = m/z
            r_j = (end_radius - beginning_radius)/number_of_radii*j + beginning_radius
            r_j1 = (end_radius - beginning_radius)/number_of_radii*(j+1) +beginning_radius
            m = 2/np.abs(r_j+r_j1)

            
        return [self.x, self.y, n, m]

class Map:
    def __init__(self, average_pixels, angle_map = [], radius_map = []):
        self.average_pixels = average_pixels
        self.size = (np.sqrt(len(average_pixels))).astype(int)

        self.angle_map = np.zeros((self.size, self.size))
        for i in range(len(self.average_pixels)):
            self.angle_map[self.average_pixels[i][0]
                           ][self.average_pixels[i][1]] = self.average_pixels[i][2]

        self.radius_map = np.zeros((self.size, self.size))
        for i in range(len(self.average_pixels)):
            self.radius_map[self.average_pixels[i][0]
                            ][self.average_pixels[i][1]] = self.average_pixels[i][3]

    def show_map(self):
        fig, ax = plt.subplots(1,2)
        fig.set_size_inches(12, 5)
        fig.set_dpi(200)

        starting_x = 0
        end_x = 2024
        starting_y = 0
        end_y = 2024

        a1 = ax[0].imshow(self.angle_map, interpolation = "none", extent=[0,size_of_img_in_nm,0,size_of_img_in_nm], cmap = "viridis")
        #ax.set_aspect(2)
        fig.colorbar(a1, ax=ax[0], label = "Relative angle [°]")
        a2 = ax[1].imshow(self.radius_map, interpolation = "none", extent=[0,size_of_img_in_nm,0,size_of_img_in_nm], cmap = "viridis")
        fig.colorbar(a2, ax=ax[1], label = "Moiré period size[nm]")
        #original = cv2.imread(photo_name + photo_format, cv2.IMREAD_GRAYSCALE)
        #a3 = ax[2].imshow(original,interpolation = "none", extent=[0,size_of_img_in_nm,0,size_of_img_in_nm], cmap = 'gray')
        #fig.colorbar(a3, ax=ax[2], label="")
        fig.tight_layout()
        plt.show()

    def save_map(self, save_to_path):
        cv2.imwrite(save_to_path + "angle_map.jpg", self.angle_map)
        cv2.imwrite(save_to_path + "radius_map.jpg", self.radius_map)

#Creating photos
def create_photos(number_of_angles, number_of_radii, name, 
                  photo_format, show = False):
    binarezed_radii = []
    binarized_angles = []

    for angle in range(0, number_of_angles):
        photo_name = name + "A" + str(angle) + photo_format
        photo = Photo(photo_name)
        if show == True:
            photo.show()
        bin_threshhold = photo.average()-2*photo.std()
        binarized_matrix = photo.binarize(bin_threshhold)
        binarized_angles.append(binarized_matrix)

    for radius in range(0, number_of_radii):
        photo_name = name + "R" + str(radius) + photo_format
        photo = Photo(photo_name)
        if show == True:
            photo.show()
        bin_threshhold = photo.average()-2*photo.std()
        binarized_matrix = photo.binarize(bin_threshhold)
        binarezed_radii.append(binarized_matrix)

    return  binarized_angles, binarezed_radii

#Creating pixels
def create_pixels(number_of_angles, number_of_radii, 
                  binarized_angles, binarezed_radii):
    
    average_pixels = []

    if save_map == True:
        for i in binarezed_radii:
            plt.imshow(i, cmap='gray')
            plt.show()  

    if save_map == True:
        for i in binarized_angles:
            plt.imshow(i, cmap='gray')
            plt.show()  


    for x in range(0, size):
        for y in range(0, size):

            matrix_of_angles = np.zeros(number_of_angles)
            matrix_of_radii = np.zeros(number_of_radii)
            
            
            for angle in range(0, number_of_angles):
                matrix_of_angles[angle] = binarized_angles[angle][x][y]
                

            for radius in range(0, number_of_radii):
                matrix_of_radii[radius] = binarezed_radii[radius][x][y]
                

            # We get a set of lists in a for of: [x, y, average_angle, average_radius]
            average_pixels.append(Pixel(x, y, matrix_of_angles, 
                                        matrix_of_radii).average())
    return average_pixels

def filtration(number_of_angles, number_of_radii, photo_name, photo_format, 
               save_to_path, show_images = False, save = False):

    binarezed_radii, binarized_angles = create_photos(number_of_angles, number_of_radii,
                                                       photo_name, photo_format, 
                                                       show_images)
    
    #print(binarezed_matrices)
    average_pixels = create_pixels(number_of_angles, number_of_radii, 
                                   binarized_angles, binarezed_radii)
    
    print(average_pixels[1])
    map = Map(average_pixels)
    map.show_map()
    if save:
        map.save_map(save_to_path)
    return map

#######################################################################################

#Some parameters to type in
#Those parameters are the same as in DM script
number = 12
number_of_angles = number
number_of_radii = number

# names should be in the format: nameoffile_angle_radius.format 
# here write only nameoffile (and path as well)
photo_name = "14.29.56 Scanning Acquire_1_0_"
#,"13.38.56 Scanning Acquire_1_","15.12.32 Scanning Acquire_1_","15.24.67 Scanning Acquire_1_","15.44.35 Scanning Acquire_1_"]
photo_format = ".jpg"
save_map_path = "map1"
save_map = False
# it doesn't save map yet, but it shows 
# all images produced in the process of mapping

#Scale adjustments
size_of_img_in_nm = 476.84
#Use VALUES choosen in test script
beginning_angle = 10
end_angle = 50
#If you can measure the real value of the angle of two twisted layers,
#use real values of the angles, not choosen ones, keep in mind that
#for angles [0,2pi] moire_angle = pi/2 - 1/2*layers_angle,
#layer_angle = pi - 2*moire_angle
#Set real_angle = True
real_angle = False

#MEASURE it from FFT created by test script
beginning_radius =  30*0.006
end_radius = 120*0.006

########################################################################################

#Those parameters can be changed but these are reccomended values for the best results 


angle_n0 = beginning_angle - beginning_angle*0.2
radius_m0 = beginning_radius - beginning_radius*0.2
print("a0 " + str(angle_n0))
print("r0 " + str(radius_m0))


#size of image in pixels
size = 2048

#Main code

map = filtration(number_of_angles, number_of_radii, photo_name, 
                 photo_format, save_map_path, brightness, contrast, save_map)