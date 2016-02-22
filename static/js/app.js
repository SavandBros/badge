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

function get_badge_url(service, action_index, format_index, package) {

    // Return a proper url of the badge based on it's service and package
    return 'http://badge.kloud51.com/'+service+'/'+services[service].actions[action_index].slug+'/'+package+'/badge.'+formats[format_index];
}

function append_action(service, action_index, format_index, package) {

    // Shortening data
    var action = services[service].actions[action_index].title;
    var url    = get_badge_url(service, action_index, format_index, package);

    // Appending to page
    $('.actions').append('\
        <div class="panel panel-default panel-body">\
            <p class="col-md-2">'+action+'</p>\
            <span class="col-md-8">\
                <input onclick="this.select()" class="form-control badge-url" readonly value="'+url+'">\
            </span>\
            <span class="col-md-2">\
                <img class="pull-right badge-image" src="'+url+'">\
            </span>\
        </div>\
    ');
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

function reinitialize(service, package) {

    // Reset badges
    $('.actions').html('');

    // Reset input value
    $('input.search').val(package);

    // Append all service badges to page based on the new settings
    for (action in services[service].actions) 
        append_action(service, action, currents.format, package);
}
}

function set_format(format_index) {

    // Save the format
    currents.format = format_index;

    // Change badges based on format
    reinitialize(currents.service, currents.package);
}
