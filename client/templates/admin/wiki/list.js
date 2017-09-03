$(function () {
    var table;
    table = $('.js-exportable').DataTable({
        "bSortClasses": false,
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel'
        ],
        "data": [
{% for item in items %}
[['{{e(item.get('name'))}}', '{{e(item.get('url', ''))}}'],
'{{e(item.get('type'))}}',
[{% for lang, i18n in item.get('i18n', {}).items(): %}
['{{e(i18n.get('url'))}}', '{{e(lang)}}', '{{e(i18n.get('name'))}}'],
{% endfor %}],
{% for admin in item.get('admin_hierarchy', {}) %}
['{{e(admin.get('url'))}}', '{{e(admin.get('name'))}}', '{{e(admin.get('type'))}}'],
{% endfor %},
'asdf', 'adsf', 'asdf', 'asdf', 'asdf', 'adsf', 'asdf'],
{% endfor %}
        ],
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