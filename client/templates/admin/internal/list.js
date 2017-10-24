$(function () {
    {% if items.count() %}
/*    console.log(
[
'{{items[0].get('code')|e}}',
'{{items[0].get('name')|e}}',
'{{items[0].get('type')|e}}',
[{% for lang, i18n in items[0].get('i18n', {}).items(): %}
['{{i18n|e}}', '{{lang|e}}'],
{% endfor %}],
{% for admin in items[0].get('admin_hierarchy', {}) %}
['{{admin.get('name')|e}}', '{{admin.get('type')|e}}'],
{% endfor %},
'{{items[0].get('capital')|e}}',
['http://maps.google.com/maps?q={{items[0].get('center', {}).get('lat')|e}},{{items[0].get('center', {}).get('lng')|e}}&ll={{items[0].get('center', {}).get('lat')|e}},{{items[0].get('center', {}).get('lng')|e}}&z=12', '{{items[0].get('center', {}).get('lat')|e}}, {{items[0].get('center', {}).get('lng')|e}}'],
[{% for borders in items[0].get('borders', {}) %}
['{{borders.get('lat')|e}}', '{{borders.get('lng')|e}}'],
{% endfor %}],
['{{items[0].get('bounds', {}).get('left',{}).get('lat')|e}}', '{{items[0].get('bounds', {}).get('left',{}).get('lng')|e}}', '{{items[0].get('bounds', {}).get('right',{}).get('lat')|e}}', '{{items[0].get('bounds', {}).get('right',{}).get('lng')|e}}'],
'{{items[0].get('altitude')|e}}',
'{{items[0].get('population')|e}}',
'{{items[0].get('density')|e}}',
'{{items[0].get('area')|e}}',
'{{items[0].get('postal_codes')|e}}',
'{{items[0].get('time')|e}}',
'{{items[0].get('other')|e}}',
'{{items[0].get('sources')|e}}',
]);*/
    {% endif %}
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
        {% for item in items %}
[
['{{url_for('internal_unit', id=e(item.get('_id')))}}', '{{url_for('internal_edit', id=e(item.get('_id')))}}', '{{url_for('internal_delete', id=e(item.get('_id')))}}'],
'{{item.get('name')|e}}',
'{{item.get('type')|e}}',
'{{ item.get('admin_hierarchy', {}).get('ADMIN_LEVEL_1', {}).get('name')|e }}',
'{{ item.get('admin_hierarchy', {}).get('ADMIN_LEVEL_2', {}).get('name')|e }}',
'{{ item.get('admin_hierarchy', {}).get('ADMIN_LEVEL_3', {}).get('name')|e }}',
'{{ item.get('admin_hierarchy', {}).get('ADMIN_LEVEL_4', {}).get('name')|e }}',
'{{ item.get('admin_hierarchy', {}).get('ADMIN_LEVEL_5', {}).get('name')|e }}',
'{{ item.get('admin_hierarchy', {}).get('ADMIN_LEVEL_6', {}).get('name')|e }}',
'{{ item.get('admin_hierarchy', {}).get('ADMIN_LEVEL_7', {}).get('name')|e }}',
'{{ item.get('admin_hierarchy', {}).get('ADMIN_LEVEL_8', {}).get('name')|e }}',
'{{item.get('capital')|e}}',
['http://maps.google.com/maps?q={{e(item.get('center', {}).get('lat'))}},{{e(item.get('center', {}).get('lng'))}}&ll={{e(item.get('center', {}).get('lat'))}},{{e(item.get('center', {}).get('lng'))}}&z=12', '{{item.get('center', {}).get('lat')}}, {{item.get('center', {}).get('lng')}}'],
'{{item.get('population')|e}}',
'{{item.get('postal_codes')|e}}'
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