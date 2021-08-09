function getNewBadge(txt) {

    let span = document.createElement("div");
    span.classList.add("uk-badge");
    span.classList.add("uk-background-secondary");
    span.id = txt;
    span.name = txt;
    span.innerText = txt;

    close = document.createElement("button");
    let att = document.createAttribute("uk-close");
    att.value = ""
    close.setAttributeNode(att);
    close.classList.add("uk-margin-small-left");

    close.addEventListener("click", function (event) {
        document.getElementById("badges").querySelector("#" + event.view.span.id).remove();
    });

    span.appendChild(close);

    return span;

}

function startTagTxt(id_input,id_btn,id_added_badges) {

    const callback = function (event) {

        let code;

        if (event.key !== undefined) {
            code = event.key;
        } else if (event.keyIdentifier !== undefined) {
            code = event.keyIdentifier;
        } else if (event.keyCode !== undefined) {
            code = event.keyCode;
        }

        if (code === 13) {

            event.preventDefault();
            let txt = document.getElementById(id_input).value.slugify();
            input.value = "";
            const digits = /\s|\W|\d/gm;
            if (digits.test(txt)) {
                return UIkit.notification({
                    message: '<span>' + 'Error to input, only words allowed.' + '</span>',
                    pos: 'top-center',
                    timeout: 1500
                });
            }

            const span = this.getNewBadge();

            document.getElementById(id_added_badges).appendChild(span);

        }
    }

    let input = document.getElementById(id_input);

    input.addEventListener("keyup", callback);

    let btn = document.getElementById(id_btn);

    btn.addEventListener("click", callback);    

}

