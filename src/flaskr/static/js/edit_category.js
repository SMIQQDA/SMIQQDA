/*
 * To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
 * Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
 * SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
 * The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
 * Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
*/

// Show the categories in the category section of the html page
function showEditableCategories(categoriesList) {

    const category = document.getElementById("category");
    category.innerHTML = ""; // Clear the list

    let buttonCategories = [];
    let buttonLabels = [];
    let buttonArchiveCategories = [];
    let buttonArchiveLabels = [];
    let buttonDeleteCategories = [];
    let buttonDeleteLabels = [];
    let currentCategory = "";
    let indexCategory = 0;

    for (let i = 0; i < categoriesList.length; i++) {

        // The category is the first item of the array and the label is the second element
        if (categoriesList[i][0] !== currentCategory) {
            if (currentCategory !== "") {
                let addLabelButton = createAddLabelButton(categoriesList[i-1][1]); // -1 to have the previous id
                category.appendChild(addLabelButton);
            }
            buttonCategories[indexCategory] = createSpan("category", categoriesList[i][0]);
            buttonCategories[indexCategory].dataset.categoryId = categoriesList[i][1];

            // Create the span where there are the archive and delete buttons for the category
            let spanCategory = document.createElement("span");
            spanCategory.classList.add("category-button");

            buttonArchiveCategories[indexCategory] = createButton("archive");
            buttonArchiveCategories[indexCategory].dataset.categoryId = categoriesList[i][1];
            if (categoriesList[i][4]) {
                buttonArchiveCategories[indexCategory].classList.add("archived");
                buttonArchiveCategories[indexCategory].innerHTML = "Unarchive";
            }

            buttonDeleteCategories[indexCategory] = createButton("delete");
            buttonDeleteCategories[indexCategory].dataset.text = categoriesList[i][0];
            buttonDeleteCategories[indexCategory].dataset.categoryId = categoriesList[i][1];

            spanCategory.appendChild(buttonArchiveCategories[indexCategory]);
            spanCategory.innerHTML += " ";
            spanCategory.appendChild(buttonDeleteCategories[indexCategory]);

            buttonCategories[indexCategory].appendChild(spanCategory);
            category.appendChild(buttonCategories[indexCategory]);

            currentCategory = categoriesList[i][0];
            indexCategory++;
        }

        // Create the span where there are the archive and delete buttons for the sub-category
        if (categoriesList[i][3]) {
            buttonLabels[i] = createSpan("sub-category", categoriesList[i][2]);
            buttonLabels[i].dataset.categoryId = categoriesList[i][1];
            buttonLabels[i].dataset.labelId = categoriesList[i][3];

            let spanCategory = document.createElement("span");
            spanCategory.classList.add("sub-category-button");

            buttonArchiveLabels[i] = createButton("sub-archive", true);
            buttonArchiveLabels[i].dataset.labelId = categoriesList[i][3];
            if (categoriesList[i][5]) {
                buttonArchiveLabels[i].classList.add("archived");
                buttonArchiveLabels[i].innerHTML = "Unarchive";
            }

            buttonDeleteLabels[i] = createButton("sub-delete", true);
            buttonDeleteLabels[i].dataset.text = categoriesList[i][2];
            buttonDeleteLabels[i].dataset.labelId = categoriesList[i][3];

            spanCategory.appendChild(buttonArchiveLabels[i]);
            spanCategory.innerHTML += " ";
            spanCategory.appendChild(buttonDeleteLabels[i]);

            buttonLabels[i].appendChild(spanCategory);
            category.appendChild(buttonLabels[i]);
        }
    }

    if(categoriesList.length > 0) {
        let addLabelButton = createAddLabelButton(categoriesList[categoriesList.length - 1][1]);
        category.appendChild(addLabelButton);
    }

    let addCategoryButton = createAddCategoryButton();
    category.appendChild(addCategoryButton);

    // Add all event trigger on the related buttons
    let subArchiveButtons = document.querySelectorAll(".sub-archive-button");
    for (var i = 0; i < subArchiveButtons.length; i++) {
        subArchiveButtons[i].addEventListener("click", archiveLabel);
    }

    let archiveButtons = document.querySelectorAll(".archive-button");
    for (var i = 0; i < archiveButtons.length; i++) {
        archiveButtons[i].addEventListener("click", archiveCategory);
    }

    let subDeleteButtons = document.querySelectorAll(".sub-delete-button");
    for (var i = 0; i < subDeleteButtons.length; i++) {
        subDeleteButtons[i].addEventListener("click", deleteLabel);
    }

    let deleteButtons = document.querySelectorAll(".delete-button");
    for (var i = 0; i < deleteButtons.length; i++) {
        deleteButtons[i].addEventListener("click", deleteCategory);
    }
}

function archiveLabel(evt) {
    archive(evt, "label");
}

function archiveCategory(evt) {
    archive(evt, "category");
}

async function archive(evt, type) {

    let path = "";
    let button = evt.currentTarget;
    button.disabled = true;
    if (type === "category") {
        path = `/api/categories/${categoryType}/${button.dataset.categoryId}`;
    } else if (type === "label") {
        path = `/api/labels/${categoryType}/${button.dataset.labelId}`;
    }

    try {
        if (button.classList.contains("archived")) {
            const response = await axios.post(`${path}/unarchive`);
            button.classList.remove("archived");
            button.innerHTML = "Archive";
        } else {
            const response = await axios.post(`${path}/archive`);
            button.classList.add("archived");
            button.innerHTML = "Unarchive";
        }
    } catch (error) {
        console.error(error);
    }
    button.disabled = false;

    return ""
}

function deleteLabel(evt) {
    _delete(evt, "label");
}

function deleteCategory(evt) {
    _delete(evt, "category");
}

async function _delete(evt, type) {

    let path = "";
    let button = evt.currentTarget;
    button.disabled = true;
    if (confirm(`Are you sure to delete the ${type} : ${button.dataset.text}`)) {
        if (confirm(`It will delete all the annotations related to the ${type} : ${button.dataset.text}`)) {
            if (type === "category") {
                path = `/api/categories/${categoryType}/${button.dataset.categoryId}`;
            } else if (type === "label") {
                path = `/api/labels/${categoryType}/${button.dataset.labelId}`;
            }

            try {
                const response = await axios.delete(path);
                let categoriesList = await listCategories(true, categoryType);
                showEditableCategories(categoriesList);
            } catch (error) {
                console.error(error);
            }
        }
    }
    button.disabled = false;

    return ""
}

function addLabel(evt) {
    _add(evt, "label");
}

function addCategory(evt) {
    _add(evt, "category");
}

async function _add(evt, type) {

    let path = "";
    let body = {};
    let button = evt.currentTarget;
    button.disabled = true;
    let title = "";

    if (type === "category") {
        title = document.getElementById("input-category").value;

        path = `/api/categories/${categoryType}/create`;
        body = {
            category_title: title
        }
    } else if (type === "label") {
        title = document.getElementById(`input-category-${button.dataset.categoryId}`).value;

        path = `/api/labels/${categoryType}/create`;
        body = {
            category_id: button.dataset.categoryId,
            label_title: title
        }
    }

    try {
        const response = await axios.post(path, body);
        console.log(response.data);
        let categoriesList = await listCategories(true, categoryType);
        showEditableCategories(categoriesList);
    } catch (error) {
        console.error(error);
    }
    button.disabled = false;

    return ""
}

function createSpan(name, innerHTML) {
    let span = document.createElement("span");
    span.classList.add(`${name}-span`);
    span.innerHTML = innerHTML;
    return span;
}

function createButton(name, isSub = false) {
    let button = document.createElement("button");
    button.classList.add(`${name}-button`);
    if (isSub) {
        name = name.slice(4); // Remove the "sub-" from the name
    }
    button.innerHTML = capitalizeFirstLetter(name);
    return button;
}

function createAddButton(name) {
    let button = document.createElement("button");
    button.classList.add(`add-${name}-button`);
    button.innerHTML = `Add ${name}`;
    return button;
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function createAddLabelButton(categoryId) {

    let addLabelSpan = document.createElement("span");

    let inputField = createInput(categoryId);
    addLabelSpan.appendChild(inputField);

    let addLabelButton = createAddButton("sub-category");
    addLabelButton.dataset.categoryId = categoryId;
    addLabelButton.addEventListener("click", addLabel);
    addLabelSpan.appendChild(addLabelButton);

    addLabelSpan.classList.add("sub-category-span");

    return addLabelSpan;
}

function createAddCategoryButton() {
    let addCategorySpan = document.createElement("span");

    let inputField = createInput();
    addCategorySpan.appendChild(inputField);

    let addCategoryButton = createAddButton("category");
    addCategoryButton.addEventListener("click", addCategory);
    addCategorySpan.appendChild(addCategoryButton);

    addCategorySpan.classList.add("category-span");

    return addCategorySpan;
}

function createInput(categoryId = -1) {
    let inputField = document.createElement("input");

    inputField.type = "text";
    if (categoryId >= 0) {
        inputField.id = `input-category-${categoryId}`;
        inputField.dataset.categoryId = categoryId;
    } else {
        inputField.id = "input-category";
    }

    return inputField;
}