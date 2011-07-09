(function( $ ){
    $(document).ready(function () {
        $('.bundleContent').hide();
        $('.bundleTitle').click(function(){
            $('.bundleContent:visible').slideUp('slow');
            $(this).next().slideDown('slow');
            return false;
        });
    });
})( jQuery );