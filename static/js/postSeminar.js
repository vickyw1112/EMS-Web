function addSession(){
    let sessionCount = document.getElementById("sessionCount").value;

    var ele;
    ele = $(
        '<h5 style="margin-top:50px">Session ' + (parseInt(sessionCount) + 1) + '</h5>'
    );
    $("#session-wrap").append(ele);

    ele = $(
        '<div class="form-group" style="margin-top: 20px">' +
        '<label>Title</label>' + 
        '<input class="form-control" type="text" name="session' + sessionCount + '_title" placeholder="Enter Session Title">' +
        '</div>'
    );
    $("#session-wrap").append(ele);

    ele = $(
        '<div class="form-group">' +
            '<div class="row">' +
                '<div class="col-md-6">' +
                    '<label>Presenter</label>' + 
                    '<input class="form-control" type="email" name="session' + sessionCount + '_presenter" placeholder="Enter Presenter\'s email" autocomplete="off" />' +
                '</div>' +
                '<div class="col-md-6">' +
                    '<label>Capacity</label>' + 
                    '<input class="form-control" type="number" name="session' + sessionCount + '_capacity" placeholder="Enter Session Capacity">' +
                '</div>' +
            '</div>' +
        '</div>'
    );
    $("#session-wrap").append(ele);
    $(document).ready(function(){
        $("input[name=session" + sessionCount + "_presenter]").autocomplete({
            serviceUrl: '/api/users',
            autoSelectFirst: true,
            onSelect: function (suggestion){
                this.value = suggestion.data;
            }
        });
    })

    ele = $(
        '<div class="form-group">' +
            '<div class="row">' +
                '<div class="col-md-6">' +
                    '<label>Start time</label>' + 
                    '<input class="form-control" type="datetime-local" name="session' + sessionCount + '_timeStart">' +
                '</div>' +
                '<div class="col-md-6">' +
                    '<label>End time</label>' + 
                    '<input class="form-control" type="datetime-local" name="session' + sessionCount + '_timeEnd">' +
                '</div>' +
            '</div>' +
        '</div>'
    );
    $("#session-wrap").append(ele);

    ele = $(
        '<div class="form-group">' +
        '<label>Description</label>' + 
        '<textarea class="form-control" style="height:125px" name="session' + sessionCount + '_description" placeholder="Enter Session Description">' +
        '</textarea>' +
        '</div>'
    );
    $("#session-wrap").append(ele);

    document.getElementById("sessionCount").value++;
}
