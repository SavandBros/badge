
var params = ['v', 'd', 'wheel', 'license', 'format', 'py_versions', 'implementation', 'status'];

function search() {

    event.preventDefault();

    var name = $('input.search').val();

    $('input.search').val('');
    $(".panel").css('opacity', 0.4);
    $('.badge-image').attr('src', '');

    $.ajax({
        url: 'https://pypi.python.org/pypi/'+name+'/json',
        type: 'GET',
        success: function(result) {
            $(".panel").css('opacity', 1);
            $(".panel").each(function(index) {
                var url = 'http://badge.kloud51.com/'+params[index]+'/'+name+'/badge.png';
                $($('.badge-url')[index]).val(url);
                $($('.badge-image')[index]).attr('src', url);
            });
        },
        error: function(result) {
            $(".panel").css('opacity', 1);
            return alert('Invalid package name.');
        }
    });

    return false;
}