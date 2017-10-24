$(function () {
    var table;
    var i = 0;
    table = $('.js-exportable').removeAttr('width').DataTable({
        columnDefs: [
            { width: 200, targets: 0 }
        ],
        fixedColumns: true,
        "autoWidth": false,
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
'{{item.get('postal_codes')|e}}',

        {% set item = itemsDic.get('wiki', {}) %}
'{{url_for('wiki_unit', id=e(item.get('_id')))}}',
['{{e(item.get('name'))}}', '{{e(item.get('url'))}}'],
'{{e(item.get('type'))}}',
[{% for admin_type, admin in item.get('admin_hierarchy', {}).items() %}
['{{e(admin.get('url'))}}', '{{e(admin.get('name'))}}', '{{e(admin.get('type'))}}'],
{% endfor %}],
['{{e(item.get('capital', {}).get('url') if item.get('capital') else 'javascript:void(0);')}}', '{{e(item.get('capital', {}).get('name'))}}'],
['http://maps.google.com/maps?q={{e(item.get('center', {}).get('lat'))}},{{e(item.get('center', {}).get('lng'))}}&ll={{e(item.get('center', {}).get('lat'))}},{{e(item.get('center', {}).get('lng'))}}&z=12', '{{item.get('center', {}).get('lat')}}, {{item.get('center', {}).get('lng')}}'],
'{{e(item.get('altitude'))}}',
'{{e(item.get('population'))}}',
'{{e(item.get('density'))}}',
'{{e(item.get('area'))}}',
'{{e(item.get('postal_codes'))}}',
'{{e(item.get('communes'))}}',
'{{e(item.get('canton_codes'))}}',
'{{e(item.get('commune_codes'))}}',

        {% set item = itemsDic.get('gmap', {}) %}
'{{url_for('gmaps_unit', id=e(item.get('_id')))}}',
'{{e(item.get('name'))}}',
'{{e(item.get('short_name'))}}',
'{{e(item.get('type'))}}',
[{% for admin_type, admin in item.get('admin_hierarchy', {}).items() %}
['{{e(admin.get('name'))}}', '{{e(admin.get('type'))}}'],
{% endfor %}],
['{{e(item.get('center', {}).get('lat'))}}','{{e(item.get('center', {}).get('lng'))}}'],
['{{e(item.get('bounds', {}).get('left',{}).get('lat'))}}', '{{e(item.get('bounds', {}).get('left',{}).get('lng'))}}', '{{e(item.get('bounds', {}).get('right',{}).get('lat'))}}', '{{e(item.get('bounds', {}).get('right',{}).get('lng'))}}'],
'{{e(item.get('postal_code'))}}',
'{{e(item.get('requests'))}}',

        {% set item = itemsDic.get('insee', {}) %}
'{{url_for('insee_code_unit', id=e(item.get('code')))}}',
'{{e(item.get('I_Code_Arrondissements'))}}',
'{{e(item.get('I_Ar'))}}',
'{{e(item.get('I_Cheflieu'))}}',
'{{e(item.get('I_Code_canton'))}}',
'{{e(item.get('I_Region'))}}',
'{{e(item.get('I_Dep'))}}',
'{{e(item.get('I_Canton'))}}',
'{{e(item.get('I_Typct'))}}',
'{{e(item.get('I_Burcentral'))}}',
'{{e(item.get('I_Tncc'))}}',
'{{e(item.get('I_Artmaj'))}}',
'{{e(item.get('I_Ncc'))}}',
'{{e(item.get('I_Armin'))}}',
'{{e(item.get('I_Nccent'))}}',
'{{e(item.get('InseeXls_CodeCommune'))}}',
'{{e(item.get('InseeXls_NameCommune'))}}',
'{{e(item.get('InseeXls_Population'))}}',
'{{e(item.get('I_Code_departament'))}}',
],
        {% endfor %}

        ],
        columnDefs: [
            // INTERNAL
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
            },
            // WIKI
            {
                render: function ( data, type, row ) {
                    return '<a href="'+ data +'" target="_blank">#</a>';
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return '<a href="'+ data[1] +'" target="_blank">'+ data[0] +'</a>';
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            //{
            //    render: function ( data, type, row ) {
            //        return data.reduce(function(previousValue, data, index) {
            //            return previousValue + '<a href="'+ data[0] +'" target="_blank">'+ data[1] +': '+ data[2] +'</a>';
            //        }, '')
            //    },
            //    targets: i++
            //},
            {
                render: function ( data, type, row ) {
                    return data.reduce(function(previousValue, data, index) {
                        return previousValue + '[<a href="'+ data[0] +'" target="_blank">'+ data[1] +'('+ data[2] +')</a>]';
                    }, '')
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
            //GMAP
            {
                render: function ( data, type, row ) {
                    return '<a href="'+ data +'" target="_blank">#</a>';
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
                    return data.reduce(function(previousValue, data, index) {
                        return previousValue + ' '+ data[0] +'('+ data[1] +') > ';
                    }, '')
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    var lat = data[0];
                    var lng = data[1];
                    return '<a href="http://maps.google.com/maps?q='+lat+','+lng+'&ll='+lat+','+lng+'&z=12" target="_blank">'+lat+', '+lng+'</a>';
                },
                targets: i++
            },
            {
                render: function ( data, type, row ) {
                    return '('+data[0]+','+data[1]+'),('+data[2]+','+data[3]+')';
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
            //INSEE
            {
                render: function ( data, type, row ) {
                    return '<a href="'+ data +'" target="_blank">#</a>';
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