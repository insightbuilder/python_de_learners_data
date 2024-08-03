# Table is made of objects, that have a shape, location, and dimensions. 
# Shape class starts with simple location, gives access to its location
# Rectangle is subclass of Shape, which has dimensions, gives access to its dimensions, 
# connects with other rectangles, and shares its dimension
# Rectangle can be moved, after it is cast into Movable Object. This class has methods, that just 
# provide the move & rotate methods
# Table has 4 legs. Legs have height, width & location with respect to top plate
# Table has a top plate. Top plate has breadth, thickness, height
# Table has views. Top, left and front
import sys
import logging
shp_logger = logging.getLogger("shaper")
shp_logger.setLevel(logging.INFO)
shp_hndl = logging.StreamHandler()
shp_form = logging.Formatter(fmt='%(message)s | %(levelname)s')
shp_hndl.setFormatter(shp_form)
shp_logger.addHandler(shp_hndl)


class Shape:
    def __init__(self, x_loc, y_loc):
        self.x = x_loc
        self.y = y_loc

    def show_loc(self):
        return f"Location is X: {self.x}, Y: {self.y}"


class Rectangle(Shape):
    def __init__(self, x_loc, y_loc, width, height):
        super(Rectangle,  self).__init__(x_loc, y_loc)
        self.height = height
        self.width = width
        self.connected = []

    def show_size(self):
        return f"Shape height is {self.height}, width is {self.width}"

    def connect_to(self, other):
        if isinstance(other, Rectangle):
            self.connected.append(other)
            other.connected.append(self)
            return "Connected Two Rectangles."
        else:
            shp_logger.info("Other is not Rectangle")


class Editable:
    def translate(self, rect_obj, tr_x, tr_y):
        # get location
        rect_obj.x += tr_x
        rect_obj.y += tr_y
        shp_logger.info("Moved the rectangle")

    def re_size(self, rect_obj, height_ch, width_ch):
        # get size
        rect_obj.height += height_ch
        rect_obj.width += width_ch
        shp_logger.info("Resized the rectangle")


class EditableSelf:
    def __init__(self, your_rect):
        self.rect = your_rect

    def translate(self, tr_x, tr_y):
        # get location
        self.rect.x += tr_x
        self.rect.y += tr_y
        shp_logger.info("Moved the rectangle")

    def re_size(self, height_ch, width_ch):
        # get size
        self.rect.height += height_ch
        self.rect.width += width_ch
        shp_logger.info("Resized the rectangle")


# Make a dummy shape with just location.
dummy = Shape(x_loc=100, y_loc=200)
shp_logger.info("Only the Shape.")
shp_logger.info(dummy)
shp_logger.info(dummy.show_loc())

inp1 = input("Continue ???")
if inp1 == 'a':
    sys.exit()
# Make a rectangle object

rect1 = Rectangle(x_loc=25, y_loc=25, width=50, height=50)
shp_logger.info("Making rectangles & showing details")

shp_logger.info(rect1.show_loc())
shp_logger.info(rect1.show_size())
print()
# Make the rectangle movable

inp1 = input("Continue ???")
if inp1 == 'a':
    sys.exit()

edit_rect = Editable()
shp_logger.info("Made rectangle editable")
edit_rect.translate(rect_obj=rect1, tr_x=50, tr_y=50)
# edit_rect.show_loc()
shp_logger.info(rect1.show_loc())

edit_rect.re_size(rect_obj=rect1, height_ch=35, width_ch=15)
# edit_rect.show_size()
shp_logger.info(rect1.show_size())
print()

self_edit = EditableSelf(your_rect=rect1)
shp_logger.info("Made rectangle editable... Again")
self_edit.translate(tr_x=50, tr_y=50)
# edit_rect.show_loc()
shp_logger.info(self_edit.rect.show_loc())

self_edit.re_size(height_ch=35, width_ch=15)
# edit_rect.show_size()
shp_logger.info(self_edit.rect.show_size())
print()

inp1 = input("Continue ???")
if inp1 == 'a':
    sys.exit()


class Table:
    def __init__(self, t_ht, t_wdt, t_bt, wood_thick) -> None:
        self.height = t_ht
        self.width = t_wdt
        self.breadth = t_bt
        self.thickness = wood_thick

    def top_plate(self):
        plate = Rectangle(x_loc=0, y_loc=0,
                          height=self.breadth,
                          width=self.width)
        shp_logger.info('The Top Plate size is: ')
        return plate.show_size()
   
    def legs(self):
        leg = Rectangle(x_loc=0, y_loc=0,
                        height=self.height - self.thickness,
                        width=self.thickness)
        shp_logger.info('The Leg size is: ')
        return leg.show_size()


your_table = Table(t_bt=40, t_ht=100, t_wdt=30, wood_thick=5)

shp_logger.info("The table details are...")
print()
shp_logger.info(your_table.top_plate())
print()
shp_logger.info(your_table.legs())
