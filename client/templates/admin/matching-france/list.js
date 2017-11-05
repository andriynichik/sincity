$(function () {
    var table;
    var i = 0;
    table = $('.js-exportable').removeAttr('width').DataTable({
        //columnDefs: [
        //    { width: 200, targets: 0 }
        //],
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
    {% set insee = itemsDic.get('insee', {}) %}
    {% set gmap = itemsDic.get('gmap', {}) %}
    {% set internal = itemsDic.get('internal', {}) %}
    {% set wiki = itemsDic.get('wiki', {}) %}
['{{url_for('internal_unit', id=e(internal.get('_id')))}}', '{{url_for('internal_edit', id=e(internal.get('_id')))}}', '{{url_for('internal_delete', id=e(internal.get('_id')))}}'],
'{{e(insee.get('InseeXls_CodeCommune'))}}',
'{{e(insee.get('InseeXls_NameCommune'))}}',
'{{e(insee.get('InseeXls_Population'))}}',
'{{internal.get('name')|e}}',
'{{internal.get('type')|e}}',
'{{ internal.get('admin_hierarchy', {}).get('ADMIN_LEVEL_1', {}).get('name')|e }}',
'{{ internal.get('admin_hierarchy', {}).get('ADMIN_LEVEL_2', {}).get('name')|e }}',
'{{ internal.get('admin_hierarchy', {}).get('ADMIN_LEVEL_3', {}).get('name')|e }}',
'{{ internal.get('admin_hierarchy', {}).get('ADMIN_LEVEL_4', {}).get('name')|e }}',
'{{ internal.get('admin_hierarchy', {}).get('ADMIN_LEVEL_5', {}).get('name')|e }}',
'{{ internal.get('admin_hierarchy', {}).get('ADMIN_LEVEL_6', {}).get('name')|e }}',
'{{ internal.get('admin_hierarchy', {}).get('ADMIN_LEVEL_7', {}).get('name')|e }}',
'{{ internal.get('admin_hierarchy', {}).get('ADMIN_LEVEL_8', {}).get('name')|e }}',
'{{internal.get('capital')|e}}',
        {% if internal.get('center') %}
['http://maps.google.com/maps?q={{e(internal.get('center', {}).get('lat'))}},{{e(internal.get('center', {}).get('lng'))}}&ll={{e(internal.get('center', {}).get('lat'))}},{{e(internal.get('center', {}).get('lng'))}}&z=12', '{{internal.get('center', {}).get('lat')}}, {{internal.get('center', {}).get('lng')}}'],
    {% else %}
[],
    {% endif %}
'{{internal.get('population')|e}}',
'{{internal.get('postal_codes')|e}}',

'{{url_for('wiki_unit', id=e(wiki.get('_id')))}}',
['{{e(wiki.get('name'))}}', '{{e(wiki.get('url'))}}'],
'{{e(wiki.get('type'))}}',
['{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_1', {}).get('url')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_1', {}).get('name')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_1', {}).get('type')|e }}'],
['{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_2', {}).get('url')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_2', {}).get('name')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_2', {}).get('type')|e }}'],
['{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_3', {}).get('url')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_3', {}).get('name')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_3', {}).get('type')|e }}'],
['{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_4', {}).get('url')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_4', {}).get('name')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_4', {}).get('type')|e }}'],
['{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_5', {}).get('url')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_5', {}).get('name')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_5', {}).get('type')|e }}'],
['{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_6', {}).get('url')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_6', {}).get('name')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_6', {}).get('type')|e }}'],
['{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_7', {}).get('url')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_7', {}).get('name')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_7', {}).get('type')|e }}'],
['{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_8', {}).get('url')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_8', {}).get('name')|e }}', '{{ wiki.get('admin_hierarchy', {}).get('ADMIN_LEVEL_8', {}).get('type')|e }}'],

['{{e(wiki.get('capital', {}).get('url') if wiki.get('capital') else 'javascript:void(0);')}}', '{{e(wiki.get('capital', {}).get('name'))}}'],
        {% if wiki.get('center') %}
['http://maps.google.com/maps?q={{e(wiki.get('center', {}).get('lat'))}},{{e(wiki.get('center', {}).get('lng'))}}&ll={{e(wiki.get('center', {}).get('lat'))}},{{e(wiki.get('center', {}).get('lng'))}}&z=12', '{{wiki.get('center', {}).get('lat')}}, {{wiki.get('center', {}).get('lng')}}'],
    {% else %}
[],
    {% endif %}
'{{e(wiki.get('altitude'))}}',
'{{e(wiki.get('population'))}}',
'{{e(wiki.get('density'))}}',
'{{e(wiki.get('area'))}}',
'{{e(wiki.get('postal_codes'))}}',
'{{e(wiki.get('communes'))}}',
'{{e(wiki.get('canton_codes'))}}',
'{{e(wiki.get('commune_codes'))}}',

'{{url_for('gmaps_unit', id=e(gmap.get('_id')))}}',
'{{e(gmap.get('name'))}}',
'{{e(gmap.get('short_name'))}}',
'{{e(gmap.get('type'))}}',
['{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_1', {}).get('name')|e }}', '{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_1', {}).get('type')|e }}'],
['{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_2', {}).get('name')|e }}', '{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_2', {}).get('type')|e }}'],
['{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_3', {}).get('name')|e }}', '{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_3', {}).get('type')|e }}'],
['{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_4', {}).get('name')|e }}', '{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_4', {}).get('type')|e }}'],
['{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_5', {}).get('name')|e }}', '{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_5', {}).get('type')|e }}'],
['{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_6', {}).get('name')|e }}', '{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_6', {}).get('type')|e }}'],
['{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_7', {}).get('name')|e }}', '{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_7', {}).get('type')|e }}'],
['{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_8', {}).get('name')|e }}', '{{ gmap.get('admin_hierarchy', {}).get('ADMIN_LEVEL_8', {}).get('type')|e }}'],
        {% if gmap.get('center') %}
['http://maps.google.com/maps?q={{e(gmap.get('center', {}).get('lat'))}},{{e(gmap.get('center', {}).get('lng'))}}&ll={{e(gmap.get('center', {}).get('lat'))}},{{e(gmap.get('center', {}).get('lng'))}}&z=12', '{{gmap.get('center', {}).get('lat')}}, {{gmap.get('center', {}).get('lng')}}'],
    {% else %}
[],
    {% endif %}
['{{e(gmap.get('bounds', {}).get('left',{}).get('lat'))}}', '{{e(gmap.get('bounds', {}).get('left',{}).get('lng'))}}', '{{e(gmap.get('bounds', {}).get('right',{}).get('lat'))}}', '{{e(gmap.get('bounds', {}).get('right',{}).get('lng'))}}'],
'{{e(gmap.get('postal_code'))}}',


'{{url_for('insee_code_unit', id=e(insee.get('code')))}}',
'{{e(insee.get('I_Code_Arrondissements'))}}',
'{{e(insee.get('I_Ar'))}}',
'{{e(insee.get('I_Cheflieu'))}}',
'{{e(insee.get('I_Code_canton'))}}',
'{{e(insee.get('I_Region'))}}',
'{{e(insee.get('I_Dep'))}}',
'{{e(insee.get('I_Canton'))}}',
'{{e(insee.get('I_Typct'))}}',
'{{e(insee.get('I_Burcentral'))}}',
'{{e(insee.get('I_Tncc'))}}',
'{{e(insee.get('I_Artmaj'))}}',
'{{e(insee.get('I_Ncc'))}}',
'{{e(insee.get('I_Armin'))}}',
'{{e(insee.get('I_Nccent'))}}',
'{{e(insee.get('I_Nccenr'))}}',
'{{e(insee.get('I_Code_departament'))}}',
'{{e(insee.get('ColResultInSnipet'))}}',
],
        {% endfor %}

        ],
        columnDefs: [
            { // INTERAL Edit/Delete
                render: function ( data, type, row ) {
                    //'<a href="'+ data[0] +'" target="_blank"><i class="material-icons">remove_red_eye</i></a>' +
                    return '<a href="'+ data[1] +'" target="_blank"><i class="material-icons">mode_edit</i></a>' +
                        '<a href="'+ data[2] +'" id="icon-delete" onclick="if(!confirm(\'Are you sure about that need to delete?\')){return false;}else{window.table.row($(this).parents(\'tr\')).remove().draw();}" target="_blank"><i class="material-icons">delete_forever</i></a>';
                },
                targets: i++
            },
            { // INSEE InseeXls_CodeCommune
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE InseeXls_NameCommune
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE InseeXls_Population
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL Name
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL Type
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL ADMIN_1
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL ADMIN_2
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL ADMIN_3
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL ADMIN_4
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL ADMIN_5
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL ADMIN_6
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL ADMIN_7
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL ADMIN_8
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL Capital
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL gmap link
                render: function ( data, type, row ) {
                    if (data.length) {
                        return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'</a>';
                    } else {
                        return 'None'
                    }
                },
                targets: i++
            },
            { // INTERNAL population
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INTERNAL postal codes
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            // WIKI
            {  // WIKI unit  link
                render: function ( data, type, row ) {
                    return '<a href="'+ data +'" target="_blank">#</a>';
                },
                targets: i++
            },
            { // WIKI name
                render: function ( data, type, row ) {
                    return '<a href="'+ data[1] +'" target="_blank">'+ data[0] +'</a>';
                },
                targets: i++
            },
            { // WIKI type
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // WIKI ADMIN_1
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'('+ data[2] +')</a>';
                },
                targets: i++
            },
            { // WIKI ADMIN_2
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'('+ data[2] +')</a>';
                },
                targets: i++
            },
            { // WIKI ADMIN_3
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'('+ data[2] +')</a>';
                },
                targets: i++
            },
            { // WIKI ADMIN_4
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'('+ data[2] +')</a>';
                },
                targets: i++
            },
            { // WIKI ADMIN_5
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'('+ data[2] +')</a>';
                },
                targets: i++
            },
            { // WIKI ADMIN_6
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'('+ data[2] +')</a>';
                },
                targets: i++
            },
            { // WIKI ADMIN_7
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'('+ data[2] +')</a>';
                },
                targets: i++
            },
            { // WIKI ADMIN_8
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'('+ data[2] +')</a>';
                },
                targets: i++
            },
            { // WIKI capital
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'</a>';
                },
                targets: i++
            },
            { // WIKI gmap link
                render: function ( data, type, row ) {
                    if (data.length) {
                        return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'</a>';
                    } else {
                        return 'None'
                    }
                },
                targets: i++
            },
            { // WIKI altitude
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // WIKI population
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // WIKI density
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // WIKI area
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // WIKI postal codes
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            {  // WIKI communes
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // WIKI canton codes
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // WIKI commune codes
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            //GMAP
            { // GMAP unit link
                render: function ( data, type, row ) {
                    return '<a href="'+ data +'" target="_blank">#</a>';
                },
                targets: i++
            },
            { // GMAP name
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // GMAP short name
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // GMAP type
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // GMAP ADMIN_1
                render: function ( data, type, row ) {
                    return data[0] +'('+ data[1] +')';
                },
                targets: i++
            },
            { // GMAP ADMIN_2
                render: function ( data, type, row ) {
                    return data[0] +'('+ data[1] +')';
                },
                targets: i++
            },
            { // GMAP ADMIN_3
                render: function ( data, type, row ) {
                    return data[0] +'('+ data[1] +')';
                },
                targets: i++
            },
            { // GMAP ADMIN_4
                render: function ( data, type, row ) {
                    return data[0] +'('+ data[1] +')';
                },
                targets: i++
            },
            { // GMAP ADMIN_5
                render: function ( data, type, row ) {
                    return data[0] +'('+ data[1] +')';
                },
                targets: i++
            },
            { // GMAP ADMIN_6
                render: function ( data, type, row ) {
                    return data[0] +'('+ data[1] +')';
                },
                targets: i++
            },
            { // GMAP ADMIN_7
                render: function ( data, type, row ) {
                    return data[0] +'('+ data[1] +')';
                },
                targets: i++
            },
            { // GMAP ADMIN_8
                render: function ( data, type, row ) {
                    return data[0] +'('+ data[1] +')';
                },
                targets: i++
            },
            { // GMAP center
                render: function ( data, type, row ) {
                    if (data.length) {
                        return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'</a>';
                    } else {
                        return 'None'
                    }
                },
                targets: i++
            },
            { // GMAP bounds
                render: function ( data, type, row ) {
                    return '('+data[0]+','+data[1]+'),('+data[2]+','+data[3]+')';
                },
                targets: i++
            },
            { // GMAP postal_code
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            //INSEE
            { // INSEE unit link
                render: function ( data, type, row ) {
                    return '<a href="'+ data +'" target="_blank">#</a>';
                },
                targets: i++
            },
            { // INSEE I_Code_Arrondissements
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Ar
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Cheflieu
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Code_canton
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Region
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Dep
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Canton
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Typct
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Burcentral
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Tncc
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Artmaj
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Ncc
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Armin
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Nccent
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Nccenr
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE I_Code_departament
                render: function ( data, type, row ) {
                    return data;
                },
                targets: i++
            },
            { // INSEE ColResultInSnipet
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