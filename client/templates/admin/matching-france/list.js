$(function () {
    var table;
    var i = 0;
    table = $('.js-exportable').removeAttr('width').DataTable({
        "bSortClasses": false,
        dom: 'Bflrtip',
        lengthMenu: [ [10, 100, 1000, -1], [10, 100, 1000, "All"] ],
        buttons: [
            {
                text: 'Create new',
                action: function ( e, dt, node, config ) {
                    window.open('{{url_for('internal_edit')}}');
                }
            },
            'csv', 'excel'
        ],
         "order": [[ 1, "asc" ]],
        data: [
        {% for itemsDic in items %}
[
    {% set item = itemsDic.get('internal', {}) %}
['{{url_for('internal_unit', id=e(item.get('_id')))}}', '{{url_for('internal_edit', id=e(item.get('_id')))}}', '{{url_for('internal_delete', id=e(item.get('_id')))}}'],
'{{item.get('name')|e}}',
'{{item.get('type')|e}}',
'{{ item.get('ADMIN_LEVEL_1')|e }}',
'{{ item.get('ADMIN_LEVEL_2')|e }}',
'{{ item.get('ADMIN_LEVEL_3')|e }}',
'{{ item.get('ADMIN_LEVEL_4')|e }}',
'{{ item.get('ADMIN_LEVEL_5')|e }}',
'{{ item.get('ADMIN_LEVEL_6')|e }}',
'{{ item.get('ADMIN_LEVEL_7')|e }}',
'{{ item.get('ADMIN_LEVEL_8')|e }}',
'{{item.get('capital')|e}}',
['http://maps.google.com/maps?q={{e(item.get('center', {}).get('lat'))}},{{e(item.get('center', {}).get('lng'))}}&ll={{e(item.get('center', {}).get('lat'))}},{{e(item.get('center', {}).get('lng'))}}&z=12', '{{item.get('center', {}).get('lat')}}, {{item.get('center', {}).get('lng')}}'],
'{{item.get('population')|e}}',
'{{item.get('postal_codes')|e}}',
        {% set item = itemsDic.get('wiki', {}) %}
        {% set item = itemsDic.get('gmap', {}) %}
        {% set item = itemsDic.get('insee', {}) %}
],
        {% endfor %}

        ],
        columnDefs: [
            {
                render: function ( data, type, row ) {
                    //'<a href="'+ data[0] +'" target="_blank"><i class="material-icons">remove_red_eye</i></a>' +
                    return '<a href="'+ data[1] +'" target="_blank"><i class="material-icons">mode_edit</i></a>' +
                        '<a href="'+ data[2] +'" id="icon-delete" onclick="if(!confirm(\'Are you sure about that need to delete?\')){return false;}else{window.table.row($(this).parents(\'tr\')).remove().draw();}" target="_blank"><i class="material-icons">delete_forever</i></a>';
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'</a>';
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            }
        ]
    });

    window.table = table;

    $.each($('[data-hide]'), function (e) {
        var column = table.column($(this).attr('data-column') );
        column.visible(false);
    } );

    $('.js-exportable').on( 'click', '#icon-delete', function () {

    } );

    $('a.toggle-link-vis').on( 'click', function (e) {
        e.preventDefault();
        var column = table.column($(this).attr('data-column'));
        column.visible(!column.visible());
    } );
});