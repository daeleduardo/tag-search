function inputTag(params) {

	if (typeof params.inputTagId === 'undefined' || document.getElementById(params.inputTagId) == null) {
		return console.error(`Not possible to add addEventListener: Property inputTagId is undefined or the element not found.`);
	}
	if (typeof params.badgesId === 'undefined' || document.getElementById(params.badgesId) == null) {
		return console.error(`Not possible to add addEventListener: Property badgesId is undefined or the element not found.`);
	}

	const slugify = (str) => {

		/* 
			Create SLUG from a string
			This function rewrite the string prototype and also 
			replace latin and other special characters.

			Forked by Gabriel Fróes - https://gist.github.com/gabrielfroes
			Original Author: Mathew Byrne - https://gist.github.com/mathewbyrne/1280286
		*/

		return str.toString().toLowerCase()
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

	const addTag = (data, event) => {

		event.preventDefault();
		const txt = document.getElementById(data.inputTagId);
		const digits = /\s|\W|\d/gm;

		if (digits.test(slugify(txt.value)) || txt.value == '') {
			const callbackOnError = (typeof data.callbackOnError !== 'undefined') ? data.callbackOnError : () => { console.error("Not possible to create label: The String Contains Non Words Chars.") };
			return callbackOnError();
		}

		const label = document.createElement("div");

		if ((typeof data.label.classes !== 'undefined') && isFilledArray(data.label.classes)) {
			data.label.classes.forEach(className => { label.classList.add(className); });
		}

		if ((typeof data.label.attributes !== 'undefined') && isFilledArray(data.label.attributes)) {
			data.label.attributes.forEach(att => {
				const attribute = document.createAttribute(att.name);
				attribute.value = att.value;
				label.setAttributeNode(attribute);
			});
		}

		const close = document.createElement("button");

		if ((typeof data.btnClose.attributes !== 'undefined') && isFilledArray(data.btnClose.attributes)) {
			data.btnClose.attributes.forEach(att => {
				const attribute = document.createAttribute(att.name);
				attribute.value = att.value;
				close.setAttributeNode(attribute);
			});
		}

		if ((typeof data.btnClose.classes !== 'undefined') && isFilledArray(data.btnClose.classes)) {
			data.btnClose.classes.forEach(className => { close.classList.add(className); });
		}

		if ((typeof data.btnClose.textContent !== 'undefined')) {
			close.textContent = data.btnClose.textContent;
		}

		label.innerText = txt.value;
		label.id = txt.value;
		label.name = `tags-[${txt.value}]`;
		txt.value = '';
		label.appendChild(close);

		document.getElementById(data.badgesId).appendChild(label);
		close.addEventListener("click", function () {
			this.parentNode.remove();
		});

	}

	const isFilledArray = (arr) => {
		return Array.isArray(arr) && (arr.length > 0)
	}

	const input = document.getElementById(params.inputTagId);

	input.addEventListener("keyup", function (event) {

		const key = event.key ?? event.keyIdentifier ?? event.keyCode;

		if (key === 13 || key === "Enter") {
			addTag(params, event);
		}
	});

	if (typeof params.btnTagId !== 'undefined' || document.getElementById(params.btnTagId) != null) {
		const btn = document.getElementById(params.btnTagId);
		btn.addEventListener("click", function (event) {
			addTag(params, event);
		});
	}

}