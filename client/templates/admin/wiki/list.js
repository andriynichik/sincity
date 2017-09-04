$(function () {
    var table;
    table = $('.js-exportable').DataTable({
        "bSortClasses": false,
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel'
        ],
        data: [
{% for item in items %}
[
['{{e(item.get('name'))}}', '{{e(item.get('url'))}}'],
'{{e(item.get('type'))}}',
[{% for lang, i18n in item.get('i18n', {}).items(): %}
['{{e(i18n.get('url'))}}', '{{e(lang)}}', '{{e(i18n.get('name'))}}'],
{% endfor %}],
{% for admin in item.get('admin_hierarchy', {}) %}
['{{e(admin.get('url'))}}', '{{e(admin.get('name'))}}', '{{e(admin.get('type'))}}'],
{% endfor %},
['{{e(item.get('capital', {}).get('url') if item.get('capital') else 'javascript:void(0);')}}', '{{e(item.get('capital', {}).get('name'))}}'],
['http://maps.google.com/maps?q={{e(item.get('center', {}).get('lat'))}},{{e(item.get('center', {}).get('lng'))}}&ll={{e(item.get('center', {}).get('lat'))}},{{e(item.get('center', {}).get('lng'))}}&z=12', '{{item.get('center', {}).get('lat')}}, {{item.get('center', {}).get('lng')}}'],
'{{e(item.get('altitude'))}}',
'{{e(item.get('population'))}}',
'{{e(item.get('density'))}}',
'{{e(item.get('area'))}}',
'{{e(item.get('postal_codes'))}}'
],
{% endfor %}
        ],
        columnDefs: [
            {
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'</a>';
                },
                targets: 0
            },
            {
                render: function ( data, type, row ) {
                    return data;
                },
                targets: [1,6,7,8,9,10]
            },
            {
                render: function ( data, type, row ) {
                    return data.reduce(function(previousValue, data, index) {
                        return previousValue + '<a href="'+ data[0] +'" target="_blank">'+ data[1] +': '+ data[2] +'</a>';
                    }, '')
                },
                targets: 2
            },
            {
                render: function ( data, type, row ) {
                    return data.reduce(function(previousValue, data, index) {
                        return previousValue + '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'('+ data[2] +')</a>';
                    }, '')
                },
                targets: 3
            },
            {
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'</a>';
                },
                targets: 4
            },
            {
                render: function ( data, type, row ) {
                    return '<a href="'+ data[0] +'" target="_blank">'+ data[1] +'</a>';
                },
                targets: 5
            },
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