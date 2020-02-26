document.addEventListener('DOMContentLoaded', function() {
    $('.block').draggable({
        helper: 'clone'
    });

    $('#editor').droppable({
        accept: '.block',
        drop: function (event, ui) {
            let code = $('#editor').val();
            let add = ui.draggable.text();
            let startPos = $('#editor').prop('selectionStart');
            let endPos = $('#editor').prop('selectionEnd');
            let pre = code.substr(0, startPos);
            let end = code.substr(endPos);
            code = pre + (pre.endsWith('\n') ? '' : '\n') + add + (code.startsWith('\n') ? '' : '\n') + end;
            $('#editor').val(code);
        }
    });
});
