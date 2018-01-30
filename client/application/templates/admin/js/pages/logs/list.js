$(function () {

    $('[data-log-close]').on('click', function(e){
        e.preventDefault();
        var a = $(this);
        $.ajax({
            url: a.attr('href'),
        }).done(function(data) {
            if (console && console.log) {
                console.log(data);
            } else {
                alert(data);
            }
            a.text(data);
        });

        a.attr('href', 'javascript:void(0);')
        a.off('click');
    });
});