from django import template
#from blocks import models
from number.models import Canvas

register = template.Library()


def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')
register.filter('cut', cut)


@register.simple_tag
def ad_square(columns, rows):
    # example: {% ad_square 1 2 %}
    
    cell_width = 43.125
    cell_height = 21.167
    
    horizontal_distance = 5
    vertical_distance = 3.528
    
    total_width = cell_width * columns + horizontal_distance * (columns - 1)
    total_height = cell_height * rows + vertical_distance * (rows - 1)
    
    square = total_width * total_height / 100

    return ("%.2f" % square)


canvas = Canvas.objects.last()
if canvas:
    
    cell_width_px = canvas.cell_width
    cell_height_px = canvas.cell_height

    @register.simple_tag
    def ad_square_by_px(block_width_px, block_height_px):
        # example: {% ad_square_by_px 100 200 %}
        
        columns = block_width_px / cell_width_px
        rows = block_height_px / cell_height_px
        
        return ad_square(columns, rows)


    @register.simple_tag
    def newspaper_maxchars(block_width_px, block_height_px):
        
        cell_width = 43.125
        cell_height = 21.167
        vertical_distance = 3.528
        columns = block_width_px / cell_width_px
        rows = block_height_px / cell_height_px
        
        maxchars = int(cell_height * rows * 26 * columns / vertical_distance)
        
        return int(maxchars)
        

        
        
        
