import pstats
import cProfile
from mosaic import Mosaic
from fractal_mosaic import FractalMosaic
from enhanced_mosaic import EnhancedMosaic

def test_speed_mosaic():
    m = Mosaic('dali')
    m.create_mosaic('karan.jpg', 10)
    m.save_as('karan_mosaic.jpg')
    
def test_speed_fractal():
    m = FractalMosaic('dali')
    m.create_mosaic('karan.jpg', 20, 60)
    m.save_as('karan_mosaic.jpg')
    
def test_speed_enhanced():
    m = EnhancedMosaic('dali')
    m.create_mosaic('karan.jpg', 20, 60)
    m.save_as('karan_mosaic.jpg')
    
if __name__ == '__main__':
    cProfile.run('test_speed_enhanced()', 'profiling_data')
    p = pstats.Stats('profiling_data')
    p.strip_dirs()
    p.sort_stats('time')
    p.print_stats(10)
    p.print_callers(10)
    p.print_callees(10)