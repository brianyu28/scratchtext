let scripts = {'Sprite1': ''};
let curSprite = 'Sprite1';

function updateSpriteSelect() {
    $('#sprite-select').empty();
    Object.keys(scripts).forEach(sprite => {
        const option = document.createElement('option');
        option.value = sprite;
        option.innerHTML = sprite;
        $('#sprite-select').append(option);
    });
}

function updateCurrentScript() {
    scripts[curSprite] = $('#editor').val();
}

document.addEventListener('DOMContentLoaded', function() {

    updateSpriteSelect();

    $('.block').draggable({
        helper: 'clone'
    });

    $('#editor').droppable({
        accept: '.block',
        drop: function (event, ui) {
            let code = $('#editor').val();
            let add = ui.draggable.data('value').replace(/\\n/g, '\n');
            let startPos = $('#editor').prop('selectionStart');
            let endPos = $('#editor').prop('selectionEnd');
            let pre = code.substr(0, startPos);
            let end = code.substr(endPos);
            code = pre + (pre.endsWith('\n') ? '' : '\n') + add + (code.startsWith('\n') ? '' : '\n') + end;
            $('#editor').val(code);
        }
    });

    $('#form').on('submit', event => {
        updateCurrentScript();
        const formData = new FormData();
        formData.append('scripts', JSON.stringify(scripts));
        formData.append('file', document.querySelector('#file-select').files[0]);
        fetch('/submit', {
            method: 'POST',
            body: formData 
        })
        .then(response => response.blob())
        .then(blob => {
            // https://stackoverflow.com/a/42274086/11102803
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'project.sb3';
            document.body.appendChild(a);
            a.click();    
            a.remove();
        });
        return false;
    });
});
