var tl;

(function( $ ){
    $(document).ready(function () {
        var eventSource = new Timeline.DefaultEventSource();
        //Setup Timeline
        var bandInfos = [
            Timeline.createBandInfo({
                eventSource:    eventSource,
                width:          "65%",
                intervalUnit:   Timeline.DateTime.MONTH,
                intervalPixels: 100
            }),
            Timeline.createBandInfo({
                eventSource:    eventSource,
                width:          "25%",
                intervalUnit:   Timeline.DateTime.YEAR,
                intervalPixels: 200
            }),
            Timeline.createBandInfo({
                eventSource:    eventSource,
                width:          "10%",
                intervalUnit:   Timeline.DateTime.DECADE,
                intervalPixels: 200
            }),
        ];
        bandInfos[1].syncWith = 0;
        bandInfos[1].highlight = true;
        bandInfos[2].syncWith = 1;
        bandInfos[2].highlight = true;
        tl = Timeline.create($('#timeline').get(0), bandInfos);
        
        //Callback for submit button
        $('#compare-bundles').submit(function(){
            if ($('#compare-bundles option:selected').length) {
                eventSource.clear();
                $('#compare-bundles option:selected').each(function(){
                    var base_url = $(this).attr('value');
                    var json_url =  base_url + '/@@json';
                    $.getJSON(json_url, function(data){
                        eventSource.loadJSON(data, base_url);
                        alert();
                    });
                });
            }
            return false;
        });
    });
    $(document).resize(function(){
        var resizeTimerID = null;
        if (resizeTimerID == null) {
            resizeTimerID = window.setTimeout(function() {
                resizeTimerID = null;
                tl.layout();
            }, 500);
        }
    });

})( jQuery );
