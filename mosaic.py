import Image
import os

class Mosaic(object):
    """ The Mosaic class. This class builds the basic photomosaic, which
    is a single picture represented as a grid of smaller component
    pictures. """
    
    def __init__(self, path):
        """ Initialize the contents of the Mosaic object. 
        
        The Mosaic object stores all the images in the directory
        specified by the string 'path'. """
        
        self.mosaic = None
        self.database = {} 
        file_names = os.listdir(path)
        
        for name in file_names:
            image_object = Image.open(os.path.join(path, name)) 
            self.database[image_object] = _get_average(image_object)
    
    def create_mosaic(self, filename, min_size):
        """ Create and store a photomosaic version of the single picture
        specified by 'filename'. """
        
        if isinstance(filename, str):
            draft = Image.open(filename)
        else:
            draft = filename
            
        width = draft.size[0]
        height = draft.size[1]
        
        if width < min_size or height < min_size:
            tile = _get_closest(draft, self.database)
            tile = tile.resize((width, height))
            draft.paste(tile) 
        else:
            quadrants = _get_quadrants(draft, width, height)
            
            draft.paste(self.create_mosaic(quadrants[0], min_size), 
                        (0, 0, width / 2, height / 2))
            draft.paste(self.create_mosaic(quadrants[1], min_size), 
                        (0, height / 2, width / 2, height))
            draft.paste(self.create_mosaic(quadrants[2], min_size), 
                        (width / 2, height / 2, width, height))
            draft.paste(self.create_mosaic(quadrants[3], min_size), 
                        (width / 2, 0, width, height / 2))
        
        self.mosaic = draft
        return draft
        
    def save_as(self, filename):
        """ Save the picture that stores the photomosaic resulting 
        from create_mosaic in a file called 'filename'. 
        
        If the photomosaic hasn't been created yet, don't save anything. """
        
        if not self.mosaic:
            pass
        else:
            self.mosaic.save(filename)
                                       
def _get_average(image):
    """ Return a tuple of the form (r, g, b). This tuple contains the 
    average red, green and blue values for an image.
    
    'image' is an Image object. """
    
    num_pixels = image.size[0] * image.size[1]
    histogram = image.histogram()
    red, green, blue = 0.0, 0.0, 0.0
    
    for i in range(256):
        red += i * histogram[i]
        green += i * histogram[i + 256]
        blue += i * histogram[i + 512]
      
    return (red / num_pixels, green / num_pixels, blue / num_pixels)
            
def _get_closest(draft, database):
    """ Return the closest entry to 'draft' from 'database'.
    
    The closest entry is the image whose average color value is closest
    to the average color value of draft.
    'draft' in an Image object. 
    'database' is a picture database. """
    
    average = _get_average(draft)
    distances = []
    
    for (tile, (r, g, b)) in database.items():
        distances.append((((r - average[0]) ** 2 +
                           (g - average[1]) ** 2 +
                           (b - average[2]) ** 2) ** 0.5, tile))
        
    return min(distances)[1]

def _get_quadrants(draft, width, height):
    """ Return a list containing the four equal quadrants of 'draft'.
    
    'draft' is an Image object. 
    'width' and 'height' are non-negative integers. """
    
    quadrant_1 = draft.crop((0, 0, width / 2, height / 2))
    quadrant_2 = draft.crop((0, height / 2, width / 2, height))
    quadrant_3 = draft.crop((width / 2, height / 2, width, height))
    quadrant_4 = draft.crop((width / 2, 0, width, height / 2))
    
    return [quadrant_1, quadrant_2, quadrant_3, quadrant_4]
