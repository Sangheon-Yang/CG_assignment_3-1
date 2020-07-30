#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below
import glfw
from OpenGL.GL import *

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

def absolute(number):
    if (number > 0.):
        return number
    else:
        return -number

def get_unitVector(V):
    len = np.sqrt(V[1]*V[1] + V[2]*V[2] + V[0]*V[0])
    return (1./len)*V


class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)


class sphere:
    def __init__(self , center , radius , color):
        self.center = center
        self.radius = radius
        self.color = color

    def is_intersect_sphere(self, udV , p):
        s= self.center-p
        if(np.dot(s,udV)*np.dot(s,udV)-np.dot(s,s)+self.radius*self.radius < 0):#판별식<0
            return False
        else:
            return True

    def get_T_in_sphere(self, udV ,p):
        s= self.center-p
        t = 9999999.9
        if(sphere.is_intersect_sphere(self , udV , p)):
            t = np.dot(s,udV) -np.sqrt(np.dot(s,udV)*np.dot(s,udV)-np.dot(s,s)+self.radius*self.radius)
        return t

class box:
    def __init__(self , minPt , maxPt , color):
        self.minPt = minPt
        self.maxPt = maxPt
        self.color = color

    def get_T_in_box(self, udv , p):
        if(udv[0] == 0. or udv[1] == 0.or udv[2] == 0. ):
            return 9999999.9
        tmin = (self.minPt[0] - p[0])/udv[0]
        tmax = (self.maxPt[0] - p[0])/udv[0]
        if(tmin > tmax):
            tmpP = tmin
            tmin = tmax
            tmax =tmpP
        
        tmin_y = (self.minPt[1] - p[1])/udv[1]
        tmax_y = (self.maxPt[1] - p[1])/udv[1]
        if(tmin_y > tmax_y):
            tmpP = tmin_y
            tmin_y = tmax_y
            tmax_y = tmpP
        
        if(tmin > tmax_y or tmax < tmin_y):
            return 9999999.9
        
        if(tmin < tmin_y):
            tmin = tmin_y
        if(tmax > tmax_y):
            tmax = tmax_y
        
        tmin_z = (self.minPt[2] - p[2])/udv[2]
        tmax_z = (self.maxPt[2] - p[2])/udv[2]
        if(tmin_z >tmax_z):
            tmpP = tmin_z
            tmin_z = tmax_z
            tmax_z = tmpP
        
        if(tmin > tmax_z or tmax < tmin_z):
            return 9999999.9
        
        if(tmin < tmin_z):
            tmin = tmin_z
        if(tmax > tmax_z):
            tmax = tmax_z
        #print (tmin , tmax)
        return tmin

#image plane 에서 x축 y축 픽셀 벡터를 구함.unit 백터를 구함.
def get_pixelplane_vector(viewDir, imageHeight, imageWidth , heightPixelsize, widthPixelsize, distance, i, j, viewUp):
    x = get_unitVector(np.cross(viewDir, viewUp))
    y = get_unitVector(np.cross(viewDir, x))
    V_index_i_j = (distance * viewDir) + (-(imageWidth/2))*x +(-(imageHeight)/2)*y + ((imageWidth/widthPixelsize)/2)*x + ((imageHeight/heightPixelsize)/2)*y + ((imageWidth/widthPixelsize)*j)*x + ((imageHeight/heightPixelsize)*i)*y
    
    return get_unitVector(V_index_i_j)

def main():

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    # set default values
    viewDir=np.array([0,0,-1]).astype(np.float)
    viewUp=np.array([0,1,0]).astype(np.float)
    ProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted
    viewWidth=1.0
    viewHeight=1.0
    projDistance=1.0
    intensity=np.array([1,1,1]).astype(np.float)  # how bright the light is.

    

    for c in root.findall('camera'):
        viewPoint =np.array(c.findtext('viewPoint').split()).astype(np.float)#point
        viewDir =get_unitVector( np.array(c.findtext('viewDir').split()).astype(np.float))#vector
        projNormal =get_unitVector( np.array(c.findtext('projNormal').split()).astype(np.float))
        viewUp = get_unitVector(np.array(c.findtext('viewUp').split()).astype(np.float))
        temp_viewWidth =np.array(c.findtext('viewWidth').split()).astype(np.float)#viewplane size
        temp_viewHeight =np.array(c.findtext('viewHeight').split()).astype(np.float)#viewplane size
        if(c.findtext('projDistance')!=None):
            temp_projDistance =np.array(c.findtext('projDistance').split()).astype(np.float)
            projDistance = temp_projDistance[0]
        viewWidth = temp_viewWidth[0]
        viewHeight = temp_viewHeight[0]
        
        print('viewpoint', viewPoint)
        print('viewDir', viewDir)
        print('projNormal', projNormal)
        print('viewUp', viewUp)
        print('viewWidth', viewWidth)
        print('viewHeight', viewHeight)
        print('projDistance', projDistance)

            
    imgSize = np.array(root.findtext('image').split()).astype(np.int)


    diffuseColor = {}
    specularColor = {}
    exponent = {}
    for c in root.findall('shader'):
        shader_name_c = c.get('name')
        #print('name', shader_name_c)
        shader_type_c = c.get('type')
        #print('type', shader_type_c)
        #lambertian & phong
        diffuseColor_c=np.array(c.findtext('diffuseColor').split()).astype(np.float)
        #print('diffuseColor', diffuseColor_c)
        diffuseColor[shader_name_c] = Color(diffuseColor_c[0],diffuseColor_c[1],diffuseColor_c[2]).toUINT8()
        #phong only
        if(c.get('type') == 'Phong'):
            specularColor_c=np.array(c.findtext('specularColor').split()).astype(np.float)
            #print('specularColor', specularColor_c)
            exponent_c = np.array(c.findtext('exponent').split()).astype(np.int)
            specularColor[shader_name_c]=Color(specularColor_c[0],specularColor_c[1],specularColor_c[2])
            exponent[shader_name_c]=exponent_c


    sphere_arr = []
    box_arr = []

    for c in root.findall('surface'):
        type_c = c.get('type')
        #print('type', type_c)
        for b in c.iter('shader'):
            ref_c = b.get('ref')
        #print('shader ref', ref)
        if(type_c == 'Sphere'):#sphere 일때
            center_c = np.array(c.findtext('center').split()).astype(np.float)
            radius_c = np.array(c.findtext('radius').split()).astype(np.float)
            sphere_arr.append( sphere(center_c , radius_c[0] , diffuseColor[ref_c]) )
        elif(type_c == 'Box'):#box 일때
            minPt_c = np.array(c.findtext('minPt').split()).astype(np.float)
            maxPt_c = np.array(c.findtext('maxPt').split()).astype(np.float)
            box_arr.append( box(minPt_c, maxPt_c, diffuseColor[ref_c]) )

    number_of_sphere = len(sphere_arr)
    number_of_box = len(box_arr)
    
    
    light_position_arr = []
    light_intensity_arr = []
    for c in root.findall('light'):
        position_c = np.array(c.findtext('position').split()).astype(np.float)
        intensity_c = np.array(c.findtext('intensity').split()).astype(np.float)
        #print('position', position_c)
        #print('instensity', intensity_c)
        light_position_arr.append(position_c)
        light_intensity_arr.append(intensity_c)
    number_of_light=len(light_intensity_arr)
    
    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0
    
    # replace the code block below!

    
    print('num_of_sphere' , number_of_sphere)
    print('num_of_box' , number_of_box)
    print('color:', diffuseColor)
    print('sphere list : ' , sphere_arr)
    print('box list : ', box_arr)
    #j = x축 , i = y축
    for i in np.arange(imgSize[1]):
        for j in np.arange(imgSize[0]):
            #randered_surface_index = -1
            randered_color = Color(0,0,0).toUINT8()
            pixelVector = get_pixelplane_vector(viewDir,  viewHeight, viewWidth , imgSize[1], imgSize[0], projDistance, i, j, viewUp)
            temp_T = 9999999.9
            #temp_t_box = 9999999.9
            
            if(number_of_sphere > 0):
                for k in np.arange(number_of_sphere):
                    if(sphere_arr[k].is_intersect_sphere(pixelVector,viewPoint)):
                        if(temp_T > sphere_arr[k].get_T_in_sphere(pixelVector,viewPoint)):
                            temp_T = sphere_arr[k].get_T_in_sphere(pixelVector,viewPoint)
                            print(temp_T)
                            randered_color = sphere_arr[k].color
        
            if(number_of_box > 0):
                for q in np.arange(number_of_box):
                    if(box_arr[q].get_T_in_box(pixelVector , viewPoint) != 9999999.9):
                        if(temp_T > box_arr[q].get_T_in_box(pixelVector , viewPoint)):
                            temp_T = box_arr[q].get_T_in_box(pixelVector , viewPoint)
                            print(temp_T)
                            randered_color = box_arr[q].color
            
            img[i][j] = randered_color


                          

#code.interact(local=dict(globals(), **locals()))
    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')
    
if __name__=="__main__":
    main()
