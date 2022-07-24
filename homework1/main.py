from abc import ABCMeta, abstractmethod
import math


class Graphics( object ) :
    _type = 'object'

    def __init__( self, object = 'object' ) :
        self._type = object
        pass

    @abstractmethod
    def get_area( self ) :
        pass


class Triangle( Graphics ) :
    _type = 'triangle'

    def __init__( self, a, b, c ) :
        super( ).__init__( 'triangle' )
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def check_is_triangle( a, b, c ) :
        return (a + b > c) & (a + c > b) & (b + c > a)

    def get_area( self ) :
        s = (self.a + self.b + self.c) / 2
        return math.sqrt( s * (s - self.a) * (s - self.b) * (s - self.c) )


class Circle( Graphics ) :
    _type = 'circle'

    def __init__( self, radius ) :
        super( ).__init__( 'circle' )
        self._radius = radius

    @classmethod
    def basic_circle( cls ) :
        return cls( 1 )

    def get_area( self ) :
        return self._radius * self._radius * math.pi


def main( ) :
    a_triangle = Triangle( 2, 3, 4 )

    objects = [ Circle.basic_circle( ) ]

    if (Triangle.check_is_triangle( 3, 4, 5 )) :
        objects.append( Triangle( 3, 4, 5 ) )

    print( 'The first triangle\'s area is', a_triangle.get_area( ) )

    for ob in objects :
        print( 'The object', ob._type, '\'s area is', ob.get_area( ) )

    print( 'The object\'s line are', a_triangle.a, a_triangle.b, a_triangle.c )
    print( Circle._type )


if __name__ == '__main__' :
    main( )
