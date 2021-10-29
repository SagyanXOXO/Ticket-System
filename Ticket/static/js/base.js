$('document').ready(function(){
    set_listeners();
    websocket_handler();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to render toast message
// Icons have four choices Info, Warning, Success and Error
var toaster = (text, background, loaderbg, textColor, transition) =>{
    $.toast({
        text: text,
        loader: true,      
        bgColor : background,  
        loaderBg: loaderbg,
        textColor: textColor,
        showHideTransition: transition,
        allowToastClose: true,
        stack: 4,
        position: 'bottom-left',  
        hideAfter: 10000   
    });
}

var set_listeners = () => {
    $('.fa-bell').on('click', () => {
        let display = $('.notification-dropdown').css('display');

        if (display == 'none')
        {
            $('.notification-dropdown').css('display', 'flex');
            notification_referesh();
        }
        else
        {
            $('.notification-dropdown').css('display', 'none');
        }
    });
}


var set_notification_viewed = () => {
    const csrftoken = getCookie('csrftoken');

    let id = [];

    $('.not-viewed').each((index, item) =>
    {
        id.push(parseInt((item.getAttribute('data-id'))));
    });

    console.log(id);
    
    $.ajax({
        url : '/notification/',
        datatype : 'json',
        type : 'POST',
        data : {
            'csrfmiddlewaretoken' : csrftoken,
            'action' : 'set_notification_viewed',
            'id' : id,
        },
        success : function(data)
        {
            console.log(data);
        }
    });  
}

var notification_referesh = () =>{
    $('.notification-dropdown').empty();
    $.ajax({
        type : 'GET',
        url : '/notification/',
        data : {
            'action' : 'get_notification'
        },
        success : function(data)
        {
            data = data.notification;
            for (let i = 0; i < data.length; i++)
            {
                let nd = $('.notification-dropdown');
                let ni = $("<div></div>");
                ni.attr('class', 'notification-item');
                ni.attr('data-id', data[i].pk);
                if (data[i].fields.viewed == false)
                {
                    ni.addClass('not-viewed');
                }
                let p = $("<p></p>");
                p.html(data[i].fields.title);
                ni.append(p);
                nd.append(ni);
                console.log(data[i].fields);
            }
            set_notification_viewed();
        }
    });
}

var websocket_handler = () => {
    const url = 'ws://' + window.location.host + '/ws/notifications/'

    const socket = new WebSocket(url);

    socket.addEventListener('message', function(e){
        data = JSON.parse(e.data);

        // Render Toast Message
        toaster(data.message, 'black', 'F4F4F4', 'white', 'slide');

        //console.log((data.message));
        notification_referesh();
    });
}