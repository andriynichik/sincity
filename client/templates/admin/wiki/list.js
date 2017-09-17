$(function () {
    {% if items.count() %}
/*    console.log(
[
['{{e(items[0].get('name'))}}', '{{e(items[0].get('url'))}}'],
'{{e(items[0].get('type'))}}',
[{% for lang, i18n in items[0].get('i18n', {}).items(): %}
['{{e(i18n.get('url'))}}', '{{e(lang)}}', '{{e(i18n.get('name'))}}'],
{% endfor %}],
{% for admin in items[0].get('admin_hierarchy', {}) %}
['{{e(admin.get('url'))}}', '{{e(admin.get('name'))}}', '{{e(admin.get('type'))}}'],
{% endfor %},
['{{e(items[0].get('capital', {}).get('url') if items[0].get('capital') else 'javascript:void(0);')}}', '{{e(items[0].get('capital', {}).get('name'))}}'],
['http://maps.google.com/maps?q={{e(items[0].get('center', {}).get('lat'))}},{{e(items[0].get('center', {}).get('lng'))}}&ll={{e(items[0].get('center', {}).get('lat'))}},{{e(items[0].get('center', {}).get('lng'))}}&z=12', '{{items[0].get('center', {}).get('lat')}}, {{items[0].get('center', {}).get('lng')}}'],
'{{e(items[0].get('altitude'))}}',
'{{e(items[0].get('population'))}}',
'{{e(items[0].get('density'))}}',
'{{e(items[0].get('area'))}}',
'{{e(items[0].get('postal_codes'))}}'
]);*/
    {% endif %}
    var table;
    var i = 0;
    table = $('.js-exportable').DataTable({
        "bSortClasses": false,
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel'
        ],
        data: [
        {% for item in items %}
[
'{{e(item.get('_id'))}}',
['{{e(item.get('name'))}}', '{{e(item.get('url'))}}'],
'{{e(item.get('type'))}}',
[{% for admin in item.get('admin_hierarchy', {}) %}
['{{e(admin.get('url'))}}', '{{e(admin.get('name'))}}', '{{e(admin.get('type'))}}'],
{% endfor %}],
['{{e(item.get('capital', {}).get('url') if item.get('capital') else 'javascript:void(0);')}}', '{{e(item.get('capital', {}).get('name'))}}'],
['http://maps.google.com/maps?q={{e(item.get('center', {}).get('lat'))}},{{e(item.get('center', {}).get('lng'))}}&ll={{e(item.get('center', {}).get('lat'))}},{{e(item.get('center', {}).get('lng'))}}&z=12', '{{item.get('center', {}).get('lat')}}, {{item.get('center', {}).get('lng')}}'],
'{{e(item.get('altitude'))}}',
'{{e(item.get('population'))}}',
'{{e(item.get('density'))}}',
'{{e(item.get('area'))}}',
'{{e(item.get('postal_codes'))}}',
'{{e(item.get('requests'))}}'
],
        {% endfor %}

        ],
        columnDefs: [
            {
                render: function ( data, type, row ) {
                    return '<a href="#'+ data +'">#</a>';
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