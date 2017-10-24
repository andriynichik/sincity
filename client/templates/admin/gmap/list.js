$(function () {
    var table;
    var i = 0;
    table = $('.js-exportable').DataTable({
        "bSortClasses": false,
        dom: 'Bflrtip',
        lengthMenu: [ [10, 100, 1000, -1], [10, 100, 1000, "All"] ],
        buttons: [
            'csv', 'excel'
        ],
        data: [
        {% for item in items %}
[
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
'{{e(item.get('requests'))}}'
],
{% endfor %}

        ],
        columnDefs: [
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