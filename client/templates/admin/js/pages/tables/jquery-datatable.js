$(function () {
    var table;
    //Exportable table
    table = $('.js-exportable').DataTable({
        dom: 'Bfrtip',
        responsive: true,
        buttons: [
            'csv', 'excel', 'pdf', 'print'
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