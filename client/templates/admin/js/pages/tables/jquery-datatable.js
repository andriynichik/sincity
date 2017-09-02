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

    $('a.toggle-link-vis').on( 'click', function (e) {
        e.preventDefault();

        // Get the column API object
        var column = table.column( $(this).attr('data-column') );

        // Toggle the visibility
        column.visible( ! column.visible() );
    } );
});