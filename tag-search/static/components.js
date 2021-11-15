/*Componentes HTML a serem inseridos na tela */
class Components {

    randomHash = () => {
        return (Math.random() + 1).toString(36).substring(7) + (Math.random() + 1).toString(36).substring(7);
    }

    placeTemplate = (data) => {
        console.log(data.name);
        return `
        <div>
            <h3 class="uk-card-title">${data.name}</h3>
            <p>${data.description}</p>
            <p><strong>Endereço: </strong>${data.address}</p>
        </div>
        `;
    }

    //id usado na busca livre e categoria na busca por grupos.
    icon = (id, category, name) => {

        const iconSize = Math.round(screen.width * 0.026);
        const gradientId = 'grad_' + this.randomHash();
        const svgId = id;

        return L.divIcon(
            {
                className: '',
                iconSize: [Math.max(iconSize, 25), Math.max(iconSize, 41)],
                html: `<svg id="${svgId}" ${category} name="${name}" height="100" width="100" viewBox="0 0 20 20">
                        <defs>
                            <linearGradient id="${gradientId}" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:rgb(255,0,0)" />
                            <stop offset="100%" style="stop-color:rgb(255, 100, 100)" />
                            </linearGradient>
                        </defs>
                        <path fill="url(#${gradientId})"  stroke-width="1.01" d="M10,0.5 C6.41,0.5 3.5,3.39 3.5,6.98 C3.5,11.83 10,19 10,19 C10,19 16.5,11.83 16.5,6.98 C16.5,3.39 13.59,0.5 10,0.5 L10,0.5 Z"></path>
                        <circle stroke="#000" cx="10" cy="6.8" r="2.3"></circle>
                        </svg>`
            });
    }

    //Template do conteúdo que é exibido no popup.
    popup = (id, marker) => {

        let place = localStorage.getItem(`place_${id}`)
        if (place !== null) {
            const components = new Components();
            return components.placeTemplate(JSON.parse(place));
        }
        fetch(`/place/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementById('csrf_token').value
            }
        }).then(function (response) {
            return response.json();
        }).then(function (data) {
            return data[0];
        }).then(function (data) {
            localStorage.setItem(`place_${id}`, JSON.stringify(data));
            return data;
        }).then(function (data) {
            const components = new Components();
            return components.placeTemplate(data)
        }).then(function (content) {
            marker.unbindPopup();
            marker.bindPopup(content).openPopup();
        }).catch(function (error) {
            UIkit.notification.closeAll();
            UIkit.notification({
                message: "<span uk-icon='icon: ban'></span> Error to get the place information.",
                status: 'danger',
                pos: 'top-center',
                timeout: 5000
            });
            console.log(error);
        });
    }
}