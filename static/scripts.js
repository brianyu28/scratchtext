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
    scripts[curSprite] = codeMirror.getValue();
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
        codeMirror.setValue(scripts[curSprite]);
    }
}

function changeSpriteSelection(name) {
    updateCurrentScript();
    curSprite = name;
    $('#sprite-select').val(name);
    codeMirror.setValue(scripts[name]);
}

document.addEventListener('DOMContentLoaded', function() {

    codeMirror = CodeMirror(document.querySelector('#codearea'), {
        'lineNumbers': 'true',
        'tabSize': 4,
        'indentUnit': 4,
    });

    updateSpriteSelect();

    $('.block').draggable({
        helper: 'clone'
    });

    $('#codearea').droppable({
        accept: '.block',
        drop: function (event, ui) {
            let cursor = codeMirror.getCursor();
            let add = ui.draggable.data('value').replace(/\\n/g, '\n') + '\n';
            codeMirror.execCommand('indentAuto');
            codeMirror.replaceSelection(add, cursor, cursor);
            codeMirror.execCommand('goLineDown');
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
        .then(response => {
            if (response.status == 500) {
                throw new Error('There was an error converting your project to Scratch.');
            }
            return response.blob();
        })
        .then(blob => {
            // https://stackoverflow.com/a/42274086/11102803
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            const file = document.querySelector('#file-select').files[0];
            if (file === undefined) {
                a.download = 'project.sb3';
            } else {
                a.download = file.name.replace('.sb3', ' (Updated).sb3');
            }
            document.body.appendChild(a);
            a.click();    
            a.remove();
        })
        .catch(err => {
            alert(err);
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
