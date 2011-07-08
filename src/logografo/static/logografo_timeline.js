var tl;

(function( $ ){
    $(document).ready(function () {
        var bandInfos = [
             Timeline.createBandInfo({
                 width:          "70%", 
                 intervalUnit:   Timeline.DateTime.MONTH, 
                 intervalPixels: 100
             }),
             Timeline.createBandInfo({
                 width:          "30%", 
                 intervalUnit:   Timeline.DateTime.YEAR, 
                 intervalPixels: 200
             })
           ];
        tl = Timeline.create($('#timeline').get(0), bandInfos);
    });
})( jQuery );
