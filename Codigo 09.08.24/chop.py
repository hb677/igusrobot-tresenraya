import math

#slices into 9 equal cuts
def slice_and_return(image):

    #location of cuts, each 1/3 of the way across the image
    location_row_cut1 = math.ceil(image.shape[0] / 3)
    location_row_cut2 = math.ceil(image.shape[0] * (2 / 3))
    location_column_cut1 = math.ceil(image.shape[1] / 3)
    location_column_cut2 = math.ceil(image.shape[1] * (2 / 3))

    #slicing the image into 9
    slice1 = image[0:location_row_cut1, 0:location_column_cut1]
    slice2 = image[0:location_row_cut1, location_column_cut1:location_column_cut2]
    slice3 = image[0:location_row_cut1, location_column_cut2:image.shape[1]]
    slice4 = image[location_row_cut1:location_row_cut2, 0:location_column_cut1]
    slice5 = image[location_row_cut1:location_row_cut2, location_column_cut1:location_column_cut2]
    slice6 = image[location_row_cut1:location_row_cut2, location_column_cut2:image.shape[1]]
    slice7 = image[location_row_cut2:image.shape[0], 0:location_column_cut1]
    slice8 = image[location_row_cut2:image.shape[0], location_column_cut1:location_column_cut2]
    slice9 = image[location_row_cut2:image.shape[0], location_column_cut2:image.shape[1]]

    return slice1, slice2, slice3, slice4, slice5, slice6, slice7, slice8, slice9

#crops an image by a given percentage assuming it's ~ a square or = a square
def crop_by_percentage(image, percentage):
    rows = image.shape[0]
    columns = image.shape[1]
    
    border = math.ceil(((rows + columns) / 2) * (percentage / 100))

    cropped = image[border:rows-border, border: columns-border]
    
    return cropped