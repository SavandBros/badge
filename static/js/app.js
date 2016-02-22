// Supported services and badges
services = {
    "pypi": {
        'title': 'PyPi',
        'default': 'html2text',
        'actions': [
            {'slug': 'v',           'title': 'Version'        },
            {'slug': 'd',           'title': 'Downloads'      },
            {'slug': 'w',           'title': 'Wheel'          },
            {'slug': 'l',           'title': 'License'        },
            {'slug': 'f',           'title': 'Format'         },
            {'slug': 'py_versions', 'title': 'Python Versions'},
            {'slug': 's',           'title': 'Status'         },
            {'slug': 'e',           'title': 'Egg'            }
        ]
    },
    "aur": {
        'title': 'AUR',
        'default': 'git-cola',
        'actions': [
            {'slug': 'v',           'title': 'Version'        },
            {'slug': 's',           'title': 'Status'         },
            {'slug': 'num_votes',   'title': 'Votes'          },
            {'slug': 'p',           'title': 'Popularity'     },
            {'slug': 'm',           'title': 'Maintainer'     }
        ]
    }
};

// Supported formats
formats = [
    "png", "svg"
];

// Setting variables
currents = {
    "service": "pypi",
    "format":  1,
    "package": services.pypi.default,
}

function get_badge_url(service_index, action_index, format_index, package) {

    return 'http://badge.kloud51.com/'+services[service_index].slug+'/'+actions[action_index].slug+'/'+package+'/badge.'+formats[format_index];
}

function append_action(service_index, action_index, format_index, package) {

    var title = actions[action_index].title;
    var url   = get_badge_url(service_index, action_index, format_index, package);

    $('.actions').append('\
        <div class="panel panel-default panel-body">\
            <p class="col-md-2">'+title+'</p>\
            <span class="col-md-8">\
                <input onclick="this.select()" class="form-control badge-url" readonly value="'+url+'">\
            </span>\
            <span class="col-md-2">\
                <img class="pull-right badge-image" src="'+url+'">\
            </span>\
        </div>\
    ');
}

function append_service(service_index) {

    $('.services').append('<li role="presentation" class="active"><a class="bg-me">'+services[service_index].title+'</a></li>');
}

function search(event) {

    event.preventDefault();

    var package = $('input.search').val();

    $('input.search').val('');
    $('.panel').css('opacity', 0.4);
    $('.badge-image').attr('src', '');

    $.ajax({
        url: 'https://pypi.python.org/pypi/'+package+'/json',
        type: 'GET',
        success: function(result) {

            $('.panel').css('opacity', 1);
            currents.package = package;
            reinitialize(0, package);
        },
        error: function(result) {

            $('.panel').css('opacity', 1);
            currents.package = 'html2text';
            reinitialize(0, 'html2text');
            alert('Invalid package name.');
        }
    });
}

function reinitialize(service_index, package) {

    $('.actions').html('');

    for (action in actions) {

        append_action(service_index, action, currents.format, package);
    }
}

function set_format(format_index) {

    // Reset varable
    currents.format = format_index;

    // Change urls to the new format
    reinitialize(0, currents.package);
}
