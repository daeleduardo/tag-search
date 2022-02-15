/**
 * Para cada local que será adicionado como marcador: 
 * Adiciona o id como o nome do local de forma higienizada.
 * Ao clicar no marcador será exibido um popup com as informações do local
 * O centro do mapa será centralizado horizontalmente abaixo verticalmente (de acordo com o zoom) para ter um maior espaço visível do popup.
 */
function addMarkerPlaces(db) {
    if (db !== null && db.length > 0) {
        const components = new Components();
        const categories = [];
        db.forEach(place => {
            
            const name = place.name.toLowerCase().replaceAll(/da |de |do /gi, '').slugify().replace(/[^\w\s]/gi, '');
            L.marker([place.latitude, place.longitude], { icon: components.icon(place.id, place.category, name) })
                .addTo(map)
                .on('click', function (e) {
                    components.popup(place.id,this);
                    const zoomLevel = Math.max(map.getZoom(), 15);
                    let bottomLat = e.latlng.lat;

                    switch (zoomLevel) {
                        case 15:
                            bottomLat = 0.00750;
                            break;
                        case 16:
                            bottomLat = 0.00350;
                            break;
                        case 17:
                            bottomLat = 0.00180;
                            break;
                        case 18:
                            bottomLat = 0.00090;
                            break;
                    }
                    map.flyTo([(e.latlng.lat + bottomLat), e.latlng.lng], zoomLevel);
                });

            if (categories.indexOf(place.category) === -1) {
                categories.push(place.category);
                document.getElementById("categories").innerHTML += `
                <a onclick="filterMarkersByCategory('${place.category}')" class="uk-text-decoration-none"><span
                class="uk-badge uk-margin-small-left">${place.category}</span></a>
                `
            }
        });
    }


    //Remove o Spinner de carregamento inicial do mapa.
    document.getElementById("map").classList.remove("uk-invisible");
    document.getElementById("spinner").classList.add("uk-invisible");

}


//Método exibe apenas os locais da categoria selecionada (se for vazio exibe todas)
function filterMarkersByCategory(category) {
    map.closePopup();
    map.flyTo([-19.852031, -43.977785], 14);
    if (category === '') {
        return document.querySelectorAll(`svg[id]`).forEach(e => e.classList.remove("uk-invisible"));
    }
    document.querySelectorAll("svg[id]").forEach(e => e.classList.add("uk-invisible"));
    document.querySelectorAll(`svg[${category}]`).forEach(e => e.classList.remove("uk-invisible"));
}


//Método exibe apenas os locais que as tags estão contidas nas palavras inseridas para pesquisa.
function filterMarkersByTags() {
    map.closePopup();
    map.flyTo([-19.852031, -43.977785], 14);
    const input = document.getElementById("txtSearch").value.slugify().replace(/[^\w]/gi, '');
    if (input === '') {
        return UIkit.notification({
            message: 'Invalid text to search',
            timeout: 2000
        });
    }

    document.querySelectorAll("svg[id]").forEach(e => e.classList.add("uk-invisible"));
    const arrInput = input.split(" ");
    let hasResult = false;

    db.forEach(place => {
        //Une todos as tags em uma única do local em uma string e verifica com base nela para diminuir o número de interações.
        const name = place.name.toLowerCase().replaceAll(/da |de |do /gi, '').slugify().replaceAll("-", ',');
        let tagsString = place.tags + "," + name;
        arrInput.forEach(txt => {
            if (tagsString.indexOf(txt) > -1) {
                const id = place.name.toLowerCase().replaceAll(/da |de |do /gi, '').slugify().replace(/[^\w\s]/gi, '');
                document.querySelectorAll(`svg[name=${id}]`).forEach(e => e.classList.remove("uk-invisible"));
                hasResult = true;
            }
        });
    });
    if (!hasResult) {
        return UIkit.notification({
            message: 'Places not found.',
            timeout: 2000
        });
    }
}

function addSlugify() {

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

}

