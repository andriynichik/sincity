$(function () {
    var table;
    //Exportable table
    table = $('.js-exportable').DataTable({
        "bSortClasses": false,
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel'
        ]
    });

    $.each($('[data-hide]'), function (e) {
        var column = table.column($(this).attr('data-column') );
        column.visible(false);
    } );

    var column = table.column($(this).attr('data-column'));

    $('a.toggle-link-vis').on( 'click', function (e) {
        e.preventDefault();
        var column = table.column($(this).attr('data-column'));
        column.visible(!column.visible());
    } );
});