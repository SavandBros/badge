services = [
    {'slug': 'pypi', 'title': 'PyPi'}
];

actions = [
    {'slug': 'v',           'title': 'Version'        },
    {'slug': 'd',           'title': 'Downloads'      },
    {'slug': 'w',           'title': 'Wheel'          },
    {'slug': 'l',           'title': 'License'        },
    {'slug': 'f',           'title': 'Format'         },
    {'slug': 'py_versions', 'title': 'Python Versions'},
    {'slug': 's',           'title': 'Status'         }
];

formats = [
    "png", "svg"
];

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
                var url = 'http://badge.kloud51.com/pypi/'+params[index]+'/'+name+'/badge.png';
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
function reinitialize(service_index, package) {

    $('.actions').html('');

    for (action in actions) {

        append_action(service_index, action, 1, package);
    }
}