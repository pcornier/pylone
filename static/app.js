var socket = io.connect('http://127.0.0.1:5000');

webix.ready(function() {
    this.grid = webix.ui({
        container: 'grid',
        view: 'datatable',
        select: 'column',
        autowidth: true,
        autoConfig: true,
        multiselect: true,
        columns: []
    });
    
    this.stack = webix.ui({
        container: 'stack',
        view: 'list',
        select:true,
        template:'<span class="rem">[x]</span> <span class="title">#title#</span>',
        onClick: {
            'rem': function(e, id) {
                socket.emit('rem_transform', id);
            },
            'title': function (e, id) {
                socket.emit('history', id);
            }
        }
    });
});

socket.emit('ready');
    
socket.on('connect', function() {
    console.log('connected');
});

socket.on('set_columns', function(cols) {
    console.log('set cols');
    grid.config.columns = [];
    cols.forEach(function(col) {
        grid.config.columns.push(col);
    });
    grid.refreshColumns();
});

socket.on('set_records', function(rows) {
    console.log('set rows');
    grid.clearAll();
    rows = JSON.parse(rows);
    rows.forEach(function(row) {
        grid.add(row);
    });
});

socket.on('update_stack', function(trans) {
    stack.clearAll();
    trans = JSON.parse(trans);
    let id = 0;
    trans.forEach(function(t) {
        stack.add({id: t.id, title: t.command});
        id = t.id;
    });
    stack.select(id);
});

socket.on('update_trans_list', function(trans) {
    $('#transformations option').remove();
    trans.forEach(function(t) {
        let opt = $('<option data-np="' + t.np + '" value="' + t.name + '">' + t.label + '</option>');
        $('#transformations').append(opt);
    });
});

$('#add_transformation').click(function() {
    var selection = grid.getSelectedId(true);
    if (selection.length) {
        var ns = $('#transformations option:selected').data('ns');
        if (ns) {
            // dialog box
        }
        var id = webix.uid();
        var command = $('#transformations').val();
        socket.emit('add_transform', {id: id, command: command, selection: grid.getSelectedId(true)});
    }
});
