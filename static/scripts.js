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

function addSprite() {
    let name = prompt('Name for new sprite:');
    if (Object.keys(scripts).includes(name)) {
        alert('Sprite with that name already exists.');
    } else {
        scripts[name] = ''; 
        updateSpriteSelect();
        changeSpriteSelection(name);
    }
}

function deleteSprite() {
    if (Object.keys(scripts).length === 1) {
        alert('Cannot delete only remaining sprite.');
    } else {
        let sprites = Object.keys(scripts);
        let index = sprites.indexOf(curSprite) - 1;
        if (index < 0)
            index = 0;
        delete scripts[curSprite];
        updateSpriteSelect();

        // Manually change sprite selection
        sprites = Object.keys(scripts);
        curSprite = sprites[index];
        console.log(curSprite);
        $('#sprite-select').val(curSprite);
        $('#editor').val(scripts[curSprite]);
    }
}

function changeSpriteSelection(name) {
    updateCurrentScript();
    curSprite = name;
    $('#sprite-select').val(name);
    $('#editor').val(scripts[name]);
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
            a.download = document.querySelector('#file-select').files[0].name.replace('.sb3', '(Updated) .sb3');
            document.body.appendChild(a);
            a.click();    
            a.remove();
        });
        return false;
    });

    $('#add').on('click', addSprite);
    $('#delete').on('click', deleteSprite);

    document.querySelector('#sprite-select').addEventListener('change', function() {
        const name = $('#sprite-select').val();
        changeSpriteSelection(name);
    });
});
