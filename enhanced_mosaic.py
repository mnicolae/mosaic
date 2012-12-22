import Image
import ImageChops
import os
from mosaic import Mosaic, _get_average, _get_closest, _get_quadrants

class EnhancedMosaic(Mosaic):
    """ The EnhancedMosaic class. This class is an enhanced version 
    of FractalMosaic. """
    
    def __init__(self, path):
        """ Initialize the contents of the EnhancedMosaic object.
        
        The EnhancedMosaic object stores all the images in the directory
        specified by the string 'path'. """
        
        super(EnhancedMosaic, self).__init__(path) 
    
    def create_mosaic(self, filename, min_size, threshold):
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
        elif _match_in_database(draft, self.database, threshold):
            draft.paste(_match_in_database(draft, self.database, threshold))
        else:
            quadrants = _get_quadrants(draft, width, height)
            
            draft.paste(self.create_mosaic(quadrants[0], min_size, threshold),
                        (0, 0, width / 2, height / 2))
            draft.paste(self.create_mosaic(quadrants[1], min_size, threshold), 
                        (0, height / 2, width / 2, height))
            draft.paste(self.create_mosaic(quadrants[2], min_size, threshold), 
                        (width / 2, height / 2, width, height))
            draft.paste(self.create_mosaic(quadrants[3], min_size, threshold), 
                        (width / 2, 0, width, height / 2))
        
        self.mosaic = draft
        return draft
    
    def save_as(self, filename):
        """ Save the picture that stores the photomosaic resulting from
        create_mosaic in a file called 'filename'.
        
        If the photomosaic hasn't been created yet, don't save anything. """
        
        super(EnhancedMosaic, self).save_as(filename)
    
def _determine_match(draft, tile, threshold):
    """ Determine if 'draft' and 'tile' match, and return 'tile' if they do. 
    Otherwise, don't return anything.
    
    Two Image objects match if the average color distance between their
    corresponding pixels is less than 'threshold'.
    'draft' and 'tile' are Image objects.
    'threshold' is a non-negative integer. """
    
    tile = tile.resize((draft.size[0], draft.size[1]))
    hybrid = ImageChops.difference(draft, tile)
    hybrid_pix = list(hybrid.getdata())
    distance = 0.0
    
    for i in range(hybrid.size[0] * hybrid.size[1]):
        distance += ((hybrid_pix[i][0] ** 2 + 
                      hybrid_pix[i][1] ** 2 + 
                      hybrid_pix[i][2] ** 2) ** 0.5)
    
    distance /= (float(hybrid.size[0] * hybrid.size[1]))
    if distance > threshold:
        pass
    else:
        return (tile, distance)
    
def _match_in_database(draft, database, threshold):
    """ Return the best Image object in 'database' to match 'draft'.
    
    Two Image objects match if the average color distance between their
    corresponding pixels is less than than 'threshold'. 
    'draft' is an Image object. 
    'database' is a picture database. 
    'threshold' is a non-negative integer. """
    
    winner = (None, 10000)
    tiles = database.keys()
    
    for tile in tiles:
        intermediate = _determine_match(draft, tile, threshold)
        if intermediate and intermediate[1] < winner[1]:
            winner = intermediate
        
    return winner[0]
