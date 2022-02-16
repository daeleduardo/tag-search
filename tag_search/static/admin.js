








document.addEventListener("DOMContentLoaded", () => {

    setTimeout(() => {
        /* 
	Create SLUG from a string
	This function rewrite the string prototype and also 
	replace latin and other special characters.
	Forked by Gabriel Froes - https://gist.github.com/gabrielfroes
	Original Author: Mathew Byrne - https://gist.github.com/mathewbyrne/1280286
 */
    if (!String.prototype.slugify) {
        String.prototype.slugify = function () {
    
        return  this.toString().toLowerCase()
        .replace(/[àÀáÁâÂãäÄÅåª]+/g, 'a')       // Special Characters #1
        .replace(/[èÈéÉêÊëË]+/g, 'e')       	// Special Characters #2
        .replace(/[ìÌíÍîÎïÏ]+/g, 'i')       	// Special Characters #3
        .replace(/[òÒóÓôÔõÕöÖº]+/g, 'o')       	// Special Characters #4
        .replace(/[ùÙúÚûÛüÜ]+/g, 'u')       	// Special Characters #5
        .replace(/[ýÝÿŸ]+/g, 'y')       		// Special Characters #6
        .replace(/[ñÑ]+/g, 'n')       			// Special Characters #7
        .replace(/[çÇ]+/g, 'c')       			// Special Characters #8
        .replace(/[ß]+/g, 'ss')       			// Special Characters #9
        .replace(/[Ææ]+/g, 'ae')       			// Special Characters #10
        .replace(/[Øøœ]+/g, 'oe')       		// Special Characters #11
        .replace(/[%]+/g, 'pct')       			// Special Characters #12
        .replace(/\s+/g, '-')           		// Replace spaces with -
        .replace(/[^\w\-]+/g, '')       		// Remove all non-word chars
        .replace(/\-\-+/g, '-')         		// Replace multiple - with single -
        .replace(/^-+/, '')             		// Trim - from start of text
        .replace(/-+$/, '');            		// Trim - from end of text
        
        };
    }
    }, 1500)

});

function loadModal(id = null) {
    
    if (id == null) {
        return loadModalAdd();
    }
    if (id != null) {
        return loadModalEdit(id);
    }

    return UIkit.modal.alert('Invalid Action!', 'danger');
}

function loadModalAdd() {

    document.getElementById('modal-title').innerText = 'Add Place';
    document.getElementById('id').value = '';
    document.getElementById('name').value = '';
    document.getElementById('coordinates').value = '';
    document.getElementById('tags').innerHTML = '';

    UIkit.notification.closeAll();
    UIkit.modal("#modal").show();
}

function loadModalEdit(id) {

    document.getElementById('modal-title').innerText = 'Edit Place';

    UIkit.notification({
        message: "<div uk-spinner='ratio: 0.5'></div> Message",
        status: 'primary',
        pos: 'top-center',
        timeout: 60000
    });

    fetch(`/place/${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementById('csrf_token').value,
            'Authorization': 'Bearer ' + getCookie('token')
        }
    }).then(function (response) {
        return response.json();
    }).then(function (data) {
            data = data[0];
            document.getElementById('modal-title').innerText = 'Edit Place';
            document.getElementById('id').value = id;
            document.getElementById('name').value = data.name;
            document.getElementById('coordinates').value = `${data.latitude},${data.longitude}`;
            
            const arrTags = data.tags.split(",");
            for (let index in arrTags) {
                const close = document.createElement("button");
                const attribute = document.createAttribute("uk-close");
				attribute.value = '';
                close.setAttributeNode(attribute);
                close.classList.add("uk-margin-small-left");
                close.addEventListener("click", function () {
                    this.parentNode.remove();
                });
                const span = document.createElement('div');
                span.classList.add('uk-badge', 'uk-background-secondary');
                span.innerText = arrTags[index];
                span.appendChild(close);
                document.getElementById('tags').appendChild(span);
            }

        }).then(function () {
            UIkit.notification.closeAll();
            UIkit.modal("#modal").show();
        })
        .catch(function (error) {
            UIkit.notification.closeAll();
            UIkit.notification({
                message: "<span uk-icon='icon: ban'></span> Error to get the place information.",
                status: 'danger',
                pos: 'top-center',
                timeout: 5000
            });
            console.error(error);
        });

}

function removePlace(id) {
    UIkit.modal.confirm('Are you sure?').then(function () {
        fetch(`/place/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementById('csrf_token').value,
                'Authorization': 'Bearer ' + getCookie('token')
            }
        }).then(function (response) {
            return response.json();
        }).then(function (response) {
            successTransition(response);
        }).catch(function (error) {
            UIkit.notification.closeAll();
            UIkit.notification({
                message: "<span uk-icon='icon: ban'></span> Error to remove place.",
                status: 'danger',
                pos: 'top-center',
                timeout: 5000
            });
            console.error(error);
        });


    }, function () {
        console.error('Rejected.')
    });

}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}



function savePlace() {

    const coords = document.getElementById('coordinates').value.trim().split(',');

    const lat = parseFloat(coords[0].trim());
    const lng = parseFloat(coords[1].trim());
    
    const tags = document.querySelectorAll("#tags div");
    const tagsArray = [];
    for (const iterator of tags) {
        tagsArray.push(iterator.innerText);
    }


    let data = {
        'name': document.getElementById('name').value,
        'category': document.getElementById('category').value.slugify(),
        'latitude': lat,
        'longitude': lng,
        'tags': tagsArray
    }

    localStorage.clear();
    if (document.getElementById('id').value != '') {
        data['id'] = document.getElementById('id').value;
        return updatePlace(data);
    }
    return addPlace(data);
}

function addPlace(params) {
    fetch('/place', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementById('csrf_token').value,
            'Authorization': 'Bearer ' + getCookie('token')
        }, body: JSON.stringify(params)
    }).then(function (response) {
        return response.json();
    }).then(function (data) {
        successTransition(data);
    }).catch(function (error) {
        errorTransition(error);
    });
}

function updatePlace(params) {
    fetch('/place', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementById('csrf_token').value,
            'Authorization': 'Bearer ' + getCookie('token')
        }, body: JSON.stringify(params)
    }).then(function (response) {
        return response.json();
    }).then(function (data) {
        successTransition(data);
    }).catch(function (error) {
        errorTransition(error);
    });
}


function successTransition(data) {
    if (data.hasOwnProperty('code')) {
        if(data.code == 401){
            return window.location.replace("/admin");
        }
        if(data.code != 200){
            return errorTransition(data);
        }
    }

    UIkit.notification({
        message: "<span uk-icon='icon: check'></span> Place information saved successfully.",
        status: 'success',
        pos: 'top-center',
        timeout: 3000
    });
    setTimeout(function () {
        location.reload();
    }, 3000);
}

function errorTransition(error) {
    console.error(error);
    const description = (error.hasOwnProperty('description')) ? error.description: '';
    UIkit.notification({
        message: `<span uk-icon='icon: ban'></span>Error to save the place.<br/>${description}`,
        status: 'danger',
        pos: 'top-center',
        timeout: 3000
    });
}


function createTxtTagComponent(){
    return inputTag(
        {
            inputTagId: 'txtTags',
            badgesId: 'tags',
            btnTagId: 'btnAddTag',
            callbackOnError: () => {
                return UIkit.notification({
                    message: '<span>' + 'Only words are allowed' + '</span>',
                    pos: 'top-center',
                    timeout: 2000
                });
            },
            label: {
                classes: ["uk-badge", "uk-background-secondary"]
            },
            btnClose: {
                classes: ["uk-margin-small-left"],
                attributes: [{ name: "uk-close", value: '' }]
            }
        }
    );
}