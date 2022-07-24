from functools import total_ordering
from sanic import HTTPResponse, Sanic, json

app = Sanic( 'test' )


@total_ordering
class Temperature( object ) :
    def __init__( self, year, no_smooth, lowess ) :
        self._year = int( year )
        self._no_smooth = float( no_smooth )
        self._lowess = float( lowess )

    def __eq__( self, other ) :
        return self._lowess == other._lowess

    def __le__( self, other ) :
        return self._lowess < other._lowess

    def __gt__( self, other ) :
        return self._lowess > other._lowess


class Analysis( ) :
    def __init__( self, begin, end, sort ) :
        self._begin = begin
        self._end = end
        self._sort = sort


class Temps( ) :
    def __init__( self, temps, analysis ) :
        self._temps = temps
        self._analysis = analysis


def read_file( ) :
    temps = [ ]
    with open( 'test.txt', 'r' ) as file :
        for line in file :
            if (line[ 0 ] == '#') :
                continue
            x = line.split( )
            y = Temperature( x[ 0 ], x[ 1 ], x[ 2 ] )
            temps.append( y )
    return temps


def get_analysis( request ) :
    # 读取文件需求
    map_begin = request.args.get( 'begin' )
    map_end = request.args.get( 'end' )
    map_sort = request.args.get( 'sort' )
    # 错误调用判断
    if (map_begin is None or not map_begin.isdigit( )) :
        return None
    if (map_end is None or not map_end.isdigit( )) :
        return None
    if (int( map_end ) < int( map_begin )) :
        return None
    if (map_sort != 'up' and map_sort != 'down') :
        return None
    # 超界判断
    ana = Analysis( int( map_begin ), int( map_end ), map_sort )
    min_year = 10000
    max_year = 0
    temps = read_file( )
    for temp in temps :
        if (temp._year > max_year) :
            max_year = temp._year
        if (temp._year < min_year) :
            min_year = temp._year
    # 超界
    if ((ana._begin > max_year) or (ana._begin < min_year) or (ana._end > max_year) or (ana._end < min_year)) :
        return None
    temp_ = [ ]
    for temp in temps :
        if (temp._year <= int( map_end ) and temp._year >= int( map_begin )) :
            temp_.append( temp )

    # 按温度排序
    if (ana._sort == 'up') :
        temp_.sort( )
    else :
        temp_.sort( reverse = True )
    # 创建变量，返回
    tp = Temps( temp_, ana )
    return tp


@app.route( '/json' )
async def json_return( request ) :
    tp = get_analysis( request )
    ana = tp._analysis
    temps = tp._temps
    js = { }
    if (ana is None) :
        return json( js )
    for temp in temps :
        if (temp._year >= ana._begin and temp._year <= ana._end) :
            js[ temp._year ] = [ { 'year' : temp._year },
                                 { 'No_Smoothing' : temp._no_smooth },
                                 { "Lowess" : temp._lowess } ]
    return json( js )


@app.route( '/xml' )
async def xml_return( request ) :
    tp = get_analysis( request )
    ana = tp._analysis
    temps = tp._temps
    text = ''
    if (ana is None) :
        return HTTPResponse( body = text, content_type = 'text/xml' )
    text += "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Document>"
    for temp in temps :
        text += '<climate>'
        text += "<year>" + str( temp._year ) + "</year>\n"
        text += "<No_Smoothing>" + str( temp._no_smooth ) + "</No_Smoothing>\n"
        text += "<Lowess>" + str( temp._lowess ) + "</Lowess>\n"
        text += '</climate>'
    text += "</Document>\n"
    return HTTPResponse( body = text, content_type = 'text/xml' )


@app.route( '/csv' )
async def csv_return( request ) :
    tp = get_analysis( request )
    ana = tp._analysis
    temps = tp._temps
    text = ''
    if (ana is None) :
        return HTTPResponse( body = text, content_type = "text/csv" )
    for temp in temps :
        text += str( temp._year ) + "," + str( temp._no_smooth ) + "," + str( temp._lowess ) + "\n"
    return HTTPResponse( body = text, content_type = "text/csv" )


def main( ) :
    app.run( host = "127.0.0.1", port = 2054 )


if __name__ == '__main__' :
    main( )
