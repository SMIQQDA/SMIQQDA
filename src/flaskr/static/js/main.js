/*
 * To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
 * Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
 * SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
 * The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
 * Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
*/

// Global
var byDate = false;
var accountsList = [];
var postsListByAccount = {};
var indexAccount = 0;
var indexPost = 0;
var accountId = 0;
var postId = 0;
var indexImage = 0;
var totalImage = 0;
var filterAccountLabelId = [];
var filterPostLabelId = [];
var totalCountAccount = 0;

function queryParamFilterAndDate(accountsList = []) {
    let queryParam = ""
    if (filterPostLabelId.length > 0 || filterAccountLabelId.length > 0 || accountsList.length > 0 || byDate) {
        queryParam = "?";
        for (let i = 0; i < filterAccountLabelId.length; i++) {
            if (i == 0 && queryParam.length > 1) {
                queryParam += "&";
            }
            if (i > 0) {
                queryParam += "&";
            }
            queryParam += "accountAnnotationId=" + filterAccountLabelId[i];
        }

        for (let i = 0; i < filterPostLabelId.length; i++) {
            if (i == 0 && queryParam.length > 1) {
                queryParam += "&";
            }
            if (i > 0) {
                queryParam += "&";
            }
            queryParam += "postAnnotationId=" + filterPostLabelId[i];
        }

        
        for (let i = 0; i < accountsList.length; i++) {
            if (i == 0 && queryParam.length > 1) {
                queryParam += "&";
            }
            if (i > 0) {
                queryParam += "&";
            }
            queryParam += "account=" + encodeURIComponent(accountsList[i]);
        }

        let inputDate = document.getElementById("date-information-input");
        
        if (inputDate) {
            let inputDateValue = inputDate.value;
            if (inputDateValue.length > 0) {
                if (queryParam.length > 1) {
                    queryParam += "&";
                }
                queryParam += "date=" + inputDateValue;
            }
        }
    }
    return queryParam;
}

// List all posts and images of an account
async function listPosts(accountName) {

    let queryParam = queryParamFilterAndDate();

    let postsList = [];
    try {
        const response = await axios.get('/api/accounts/' + accountName + '/posts' + queryParam);
        postsList = response.data;
        console.log("Posts list", postsList);
    } catch (error) {
        console.error(error);
    }
    return postsList;
}

// List all accounts of a directory
async function listAccounts(onlyAccount = false) {

    let queryParam = queryParamFilterAndDate();

    if (onlyAccount) {
        if (queryParam.length > 0) {
            queryParam += "&accountOnly=true"
        } else {
            queryParam = "?accountOnly=true"
        }
    }

    let accountsList = [];
    try {
        const response = await axios.get('/api/accounts' + queryParam);
        accountsList = response.data;
        console.log("Account list : ", accountsList);
        if(accountsList.length <= 0) {
            alert("The filter returns no result");
        }
    } catch (error) {
        console.error(error);
    }
    return accountsList;
}

// Get post info
async function getPost(indexAccount, indexPost) {
    let accountName = accountsList[indexAccount];
    let postName = postsListByAccount[accountName][indexPost]
    let postInfo = {};
    if (accountName && postName) {
        try {
            const response = await axios.get('/api/accounts/' + accountName + '/posts/' + postName);
            postInfo = response.data;
            console.log("Post info : ", response);
        } catch (error) {
            console.error(error);
        }
    }
    return postInfo;
}

// Count the number of posts for all accounts
async function countPosts(accountsList) {

    let queryParam = queryParamFilterAndDate(accountsList);

    let postsCount = 0;
    try {
        const response = await axios.get('/api/count/posts' + queryParam);
        postsCount = response.data;
        console.log("Posts count", postsCount);
    } catch (error) {
        console.error(error);
    }
    return postsCount;
}

// Update the field by its id
function updateField(id, value) {
    if(value == null) {
        value = 'n/a';
    }
    document.getElementById(id).innerHTML = value;
}

async function showAnnotation(postId) {

    // Get the annotations of the post and select the buttons
    try {
        const response = await axios.get('/api/annotations?postId=' + postId);
        annotationList = response.data;
        console.log("Annotation : ", annotationList); // First element = id, second = label_id

        // Reset all buttons state
        selectedButtons = document.querySelectorAll(`.category-selected`);
        for (let i = 0; i < selectedButtons.length; i++) {
            selectedButtons[i].classList.remove('category-selected');
        }
        
        annotationList.forEach(annotation => {
            button = document.querySelector(`[data-label-id='${annotation[1]}']`);
            if (button) {
                button.classList.add("category-selected");
                button.dataset.annotationId = annotation[0];
            }
        });
    } catch (error) {
        console.error(error);
    }
}

async function showAccountAnnotation(accountId) {

    
    // Get the annotations of the post and select the buttons
    try {
        const response = await axios.get('/api/account_annotations?accountId=' + accountId);
        annotationList = response.data;
        console.log("Annotation : ", annotationList); // First element = id, second = label_id

        // Reset all buttons state
        selectedButtons = document.querySelectorAll(`.category-selected`);
        for (let i = 0; i < selectedButtons.length; i++) {
            selectedButtons[i].classList.remove('category-selected');
        }

        annotationList.forEach(annotation => {
            button = document.querySelector(`[data-label-id='${annotation[1]}']`);
            if (button) {
                button.classList.add("category-selected");
                button.dataset.annotationId = annotation[0];
            }
        });
    } catch (error) {
        console.error(error);
    }
}

async function showFreeAnnotation(postId) {

    // Get the annotations of the post and select the buttons
    try {
        const response = await axios.get('/api/free_annotations?postId=' + postId);
        annotationList = response.data;
        console.log("Free annotation : ", annotationList); // First element = id, second = free_text
        if (annotationList.length > 0) {
            document.getElementById("free-textarea").value = annotationList[0][1];
        } else {
            document.getElementById("free-textarea").value = "";
        }
    } catch (error) {
        console.error(error);
    }
}

async function showFreeAccountAnnotation(accountId) {

    // Get the annotations of the post and select the buttons
    try {
        const response = await axios.get('/api/free_account_annotations?accountId=' + accountId);
        annotationList = response.data;
        console.log("Free annotation : ", annotationList); // First element = id, second = free_text
        if (annotationList.length > 0) {
            document.getElementById("free-textarea").value = annotationList[0][1];
        } else {
            document.getElementById("free-textarea").value = "";
        }
    } catch (error) {
        console.error(error);
    }
}

// Show the image associated to the index, the post index and the account index
async function showImage(indexAccount, indexPost, indexImage) {
    let accountName = accountsList[indexAccount];
    let timestamp = new Date(Date.parse(document.getElementById("post-date").dataset.dateString));
    let formatted_date = `${('0' + timestamp.getDate()).slice(-2)}-${('0' + (timestamp.getMonth()+1)).slice(-2)}-${timestamp.getFullYear()%100}_${('0' + timestamp.getHours()).slice(-2)}-${('0' + timestamp.getMinutes()).slice(-2)}-${('0' + timestamp.getSeconds()).slice(-2)}`;
    let imgName = `${accountName}_${formatted_date}_${(indexImage + 1)}_${totalImage}`;

    let img = document.getElementById("post-image");

    img.src = `static/insta/comptes/${accountName}/${imgName}.jpg`;
    img.onload = function () {
        window.URL.revokeObjectURL(this.src);
    }

    updateField("post-image-current-index", indexImage + 1);
}

async function showAccountImage(accountName) {

    let img = document.getElementById("account-image");

    img.src = `static/insta/profilepictures/${accountName}_pic.jpg`;
    img.onload = function () {
        window.URL.revokeObjectURL(this.src);
    }
}

// Show the information of the post associated to the post index and the account index, show the first image
async function showPost(indexAccount, indexPost) {
    let jsonParsed = await getPost(indexAccount, indexPost);
    console.log(jsonParsed);

    // Use postId (added by the backend) instead of the id in the json to be consistent with the id stored in database
    if (jsonParsed.postId) {
        postId = jsonParsed.postId;
    }

    let date = new Date(jsonParsed.timestamp)

    // Show the new line in html and create link
    if (jsonParsed.caption) {
        jsonParsed.caption = jsonParsed.caption.replaceAll('\n', '<br/>');
        jsonParsed.caption = urlify(jsonParsed.caption);
    }

    totalImage = jsonParsed.totalImage;

    updateField("post-current-index", indexPost + 1);
    updateField("post-date", date.toLocaleString('fr-FR'));
    document.getElementById("post-date").dataset.dateString = date.toString()
    updateField("post-localisation", jsonParsed.localisation);
    updateField("post-nbr-like", jsonParsed.likesCount);
    updateField("post-nbr-comment", jsonParsed.commentsCount);
    updateField("post-caption", jsonParsed.caption);
    updateField("account-fullname", jsonParsed.ownerFullName); // it is the only place where the info is available
    updateField("post-image-total-index", jsonParsed.totalImage);
    updateField("post-type", jsonParsed.type);
    document.getElementById("post-url").href = jsonParsed.url;
    updateField("account-posts-count", jsonParsed.postsCount);
    updateField("account-posts-actually-count", jsonParsed.postsReallyCollected);
    updateField("account-posts-missing-count", jsonParsed.postsMissing);
    updateField("account-followers-count", jsonParsed.followersCount);
    updateField("account-follows-count", jsonParsed.followsCount);

    // Reset to first image
    indexImage = 0;
    await showImage(indexAccount, indexPost, indexImage);
    await showAnnotation(postId);
    await showFreeAnnotation(postId);
}

// Show the information of the account associated to the index and show the first post
async function showAccount(indexAccount, forceRefresh = false, onlyAccount = false, indexPostArg = 0) {

    let accountName = accountsList[indexAccount];
    if (accountName) {
        if (!onlyAccount && (forceRefresh || !postsListByAccount[accountName])) {
            postsListByAccount[accountName] = await listPosts(accountName);
            console.log("This is an account : ", accountName);
        }

        updateField("account-current-index", indexAccount + 1);
        updateField("account-username", accountName);
        updateField("account-total-index-no-filter", totalCountAccount);
        updateField("account-total-index", accountsList.length);
        accountId = await updateAccountInformation(accountName, onlyAccount);
        if (onlyAccount) {
            await showAccountImage(accountName);
            await showAccountAnnotation(accountId);
            await showFreeAccountAnnotation(accountId);
        } else {
            updateField("post-total-index", postsListByAccount[accountName].length);
            // Reset to first post
            indexPost = indexPostArg;
            await showPost(indexAccount, indexPost);
        }
    }
}

function urlify(text) {
    var urlRegex = /(((https?:\/\/)|(www\.))[^\s]+)/g;
    if(text != null) {
        return text.replace(urlRegex, function(url,b,c) {
            var url2 = (c == 'www.') ?  'https://' +url : url;
            return '<a href="' +url2+ '" target="_blank" rel="noopener noreferrer">' + url + '</a>';
        }) 
    } else {
        text = "n/a";
    }
    return text;
}

async function updateAccountInformation(accountName, onlyAccount) {
    try {
        const response = await axios.get('/api/accounts/' + accountName);
        let jsonParsed = response.data;
        console.log("Account info : ", jsonParsed);

        // Turn the username into link
        if(jsonParsed.account) {
            document.getElementById("account-username-url").href = `https://www.instagram.com/${jsonParsed.account}`;
        }

        let accountId = jsonParsed.idAccount;
        
        if(onlyAccount) {
            // Show the new line in html and create link
            if (jsonParsed.fullName) {
                jsonParsed.fullName = jsonParsed.fullName.replaceAll('\n', '<br/>');
                jsonParsed.fullName = urlify(jsonParsed.fullName);
            }
            updateField("account-fullname", jsonParsed.fullName);
            updateField("account-biography", jsonParsed.biography);
            updateField("account-external-url", urlify(jsonParsed.externalUrl));
            updateField("account-posts-count", jsonParsed.postsCount);
            updateField("account-posts-actually-count", jsonParsed.postsReallyCollected);
            updateField("account-posts-missing-count", jsonParsed.postsMissing);
            updateField("account-followers-count", jsonParsed.followersCount);
            updateField("account-follows-count", jsonParsed.followsCount);
        }

        return accountId
    } catch (error) {
        console.error(error);
    }
}

// List all categories
async function listCategories(selectAll = false, categoryType = "") {
    let categoriesList = [];
    let queryParam = "";
    if (selectAll) {
        console.log("Select all !");
        queryParam = "?selectAll=true";
    }
    try {
        const response = await axios.get(`/api/categories/${categoryType}${queryParam}`);
        categoriesList = response.data;
        console.log(categoriesList);
    } catch (error) {
        console.error(error);
    }
    return categoriesList;
}

// Show the categories in the category section of the html page
function showCategories(categoriesList, onlyAccount = false) {

    const category = document.getElementById("category-content");
    category.innerHTML = ""; // Clear the list

    let button = [];
    let currentCategory = "";

    for (let i = 0; i < categoriesList.length; i++) {
        button[i] = document.createElement("button");
        button[i].classList.add("category-button");

        // The category is the first item of the array and the label is the second element
        // Then it create a span element with the category and a button for each label
        if (categoriesList[i][0] !== currentCategory) {
            let spanCategory = document.createElement("span");
            currentCategory = categoriesList[i][0];
            spanCategory.innerHTML = categoriesList[i][0] + " :";
            category.appendChild(spanCategory);
        }

        button[i].dataset.categoryId = categoriesList[i][1];
        button[i].dataset.labelId = categoriesList[i][3];
        button[i].innerHTML = categoriesList[i][2];
        category.appendChild(button[i]);
    }

    var updateSelectClass = function (evt) {
        // this = evt.currentTarget = the clicked button
        console.log("Button clicked with id :", this.dataset.categoryId, this.dataset.labelId);
        this.classList.contains("category-selected") ? removeAnnotation(this, onlyAccount) : addAnnotation(this, onlyAccount);
    }

    for (var i = 0; i < button.length; i++) {
        button[i].addEventListener("click", updateSelectClass);
    }
}

async function removeAnnotation(clickedButton, onlyAccount) {
    // Block all buttons state
    categoryButtons = document.querySelectorAll(`.category-button[data-category-id="${clickedButton.dataset.categoryId}"]`);
    for (let i = 0; i < categoryButtons.length; i++) {
        categoryButtons[i].disabled = true;
    }
    clickedButton.classList.remove('category-selected');
    console.log("Remove annotation :", clickedButton.dataset.categoryId, clickedButton.dataset.labelId);
    let categoryId = clickedButton.dataset.categoryId;
    try {
        path = `/api/annotations/${postId}/`;
        if (onlyAccount) {
            path = `/api/account_annotations/${accountId}/`;
        }
        const response = await axios.delete(path + categoryId);
        if (response.data > 0) {
            console.log("Deleted annotation for category :", categoryId);
        } else {
            console.log("No deletion of annotation for category :", categoryId);
        }
    } catch (error) {
        console.error(error);
    }
    // Unblock all buttons state
    categoryButtons = document.querySelectorAll(`.category-button[data-category-id="${clickedButton.dataset.categoryId}"]`);
    for (let i = 0; i < categoryButtons.length; i++) {
        categoryButtons[i].disabled = false;
    }
}

async function addAnnotation(clickedButton, onlyAccount) {
    // Block all buttons state
    categoryButtons = document.querySelectorAll(`.category-button[data-category-id="${clickedButton.dataset.categoryId}"]`);
    for (let i = 0; i < categoryButtons.length; i++) {
        categoryButtons[i].disabled = true;
    }
    oldButton = document.querySelectorAll(`.category-selected[data-category-id="${clickedButton.dataset.categoryId}"]`);
    if (oldButton && oldButton.length > 0) {
        await removeAnnotation(oldButton[0], onlyAccount);
    } else {
        // In case of incoherent state, the old button doesn't exist but we need to delete the annotation with the categoryId then we use the current clicked button
        await removeAnnotation(clickedButton, onlyAccount);
    }

    let annotationId = 0;
    try {
        let response;
        if (onlyAccount) {
            response = await axios.post('/api/account_annotations/create', {
                account_id: accountId,
                category_id: clickedButton.dataset.categoryId,
                label_id: clickedButton.dataset.labelId
            });
        } else {
            response = await axios.post('/api/annotations/create', {
                post_id: postId,
                category_id: clickedButton.dataset.categoryId,
                label_id: clickedButton.dataset.labelId
            });
        }
        annotationId = response.data;
        clickedButton.classList.add("category-selected");
        console.log("Add annotation :", clickedButton.dataset.categoryId, clickedButton.dataset.labelId);
        console.log("Annotation id :", annotationId);
        clickedButton.dataset.annotationId = annotationId;
    } catch (error) {
        console.error(error);
    }
    // Unblock all buttons state
    categoryButtons = document.querySelectorAll(`.category-button[data-category-id="${clickedButton.dataset.categoryId}"]`);
    for (let i = 0; i < categoryButtons.length; i++) {
        categoryButtons[i].disabled = false;
    }
}

// Show the choices in the dropdown generated by Choices (JS)
function showFilterChoices(categoryType, categoriesList) {
    console.log(`Categorie list for choices ${categoryType} : ${categoriesList}`);
    let currentCategory = "";
    let choicesValues = [];
    let group = {}
    for (let i = 0; i < categoriesList.length; i++) {

        // The category is the first item of the array and the label is the second element
        // Then it create a group with the category and a choice for each label
        if (categoriesList[i][0] !== currentCategory) {
            if (i > 0) {
                choicesValues.push(group);
            }
            currentCategory = categoriesList[i][0];
            group = {
                label: categoriesList[i][0],
                choices: []
            }
        }

        group.choices.push({
            value: categoriesList[i][3],
            label: categoriesList[i][2]
        })
    }

    choicesValues.push(group); // push the last group
    if(categoryType === "account") {
        choiceAccountFilter.setChoices(choicesValues);
    } else {
        choicePostFilter.setChoices(choicesValues);
    }
}

// Get the choices (label_id) and filter the accounts and the posts
async function filterChoices(onlyAccount = false) {

    let choicesAccountValues = choiceAccountFilter.getValue(true);
    console.log("Account choices value : ", choicesAccountValues);
    console.log(`Filter account label id : ${filterAccountLabelId}`);

    let choicesPostValues = [];
    if(!onlyAccount) {
        choicesPostValues = choicePostFilter.getValue(true);
        console.log("Post choices value : ", choicesPostValues);
        console.log(`Filter post label id : ${filterPostLabelId}`);
    }


    // If new filters, then refresh (it prevent refresh if no changes)
    if ((JSON.stringify(choicesAccountValues) !== JSON.stringify(filterAccountLabelId) || JSON.stringify(choicesPostValues) !== JSON.stringify(filterPostLabelId))) {
        filterAccountLabelId = choicesAccountValues;
        filterPostLabelId = choicesPostValues;

        // Refresh the account and then the posts
        indexAccount = 0;
        let tmpAccountsList = await listAccounts(onlyAccount);
        if(tmpAccountsList.length > 0) {
            accountsList = tmpAccountsList;
            let totalCountPosts = await countPosts(tmpAccountsList);
            if(!onlyAccount) {
                updateField("post-total-index-filter", totalCountPosts);
            }
            showAccountChoices(accountsList);
            showAccount(indexAccount, true, onlyAccount);
        }
    }
}

// Show the choices in the dropdown generated by Choices (JS)
function showAccountChoices(accountsList) {
    console.log("Account list for choices : ", accountsList);

    let choicesValues = [];
    for (let i = 0; i < accountsList.length; i++) {
        choicesValues.push({
            value: accountsList[i],
            label: accountsList[i]
        })
    }

    choiceAccount.setChoices(choicesValues, 'value', 'label', true);
}

// Get the choices (account name) and show this account
async function accountChoices(onlyAccount = false) {
    let choicesValue = choiceAccount.getValue(true);
    console.log("Choices value : ", choicesValue);
    console.log("Filter label id :", filterAccountLabelId);

    indexAccount = accountsList.indexOf(choicesValue);
    showAccount(indexAccount, false, onlyAccount);
    choiceAccount.removeActiveItems();
}

// Open the directory account, list the accounts, show the first account and its first post
async function openDirectory(categoryType) {

    let onlyAccount = (categoryType === "account") ? true : false;

    // choiceFilter, choiceAccount are defined in index.html
    let accountCategoriesList = await listCategories(false, 'account');
    let categoriesList = accountCategoriesList;
    let postCategoriesList = [];

    if(!onlyAccount) {
        postCategoriesList = await listCategories(false, 'post');
        categoriesList = postCategoriesList
    }

    showCategories(categoriesList, onlyAccount); // Must be done before account > post because the showPost will call showAnnotation which required the categories
    showFilterChoices('account', accountCategoriesList);

    if(!onlyAccount) {
        showFilterChoices('post', postCategoriesList);
    }
    refreshAccount(false, onlyAccount);
}

async function refreshAccount(forceRefresh = false, onlyAccount = false) {
    indexAccount = 0;
    let tmpAccountsList = await listAccounts(onlyAccount);
    
    let totalCountPosts = 0;
    if(!onlyAccount) {
        totalCountPosts = await countPosts(tmpAccountsList);
        updateField("post-total-index-filter", totalCountPosts);
    }
    
    if(tmpAccountsList.length > 0) {
        accountsList = tmpAccountsList;
        // Set the total number of accounts only the first time this function is called (i.e when the page is displayed)
        if(totalCountAccount == 0) {
            totalCountAccount = accountsList.length;
            if(!onlyAccount) {
                updateField("post-total-index-no-filter", totalCountPosts);
            }
        }
        showAccountChoices(accountsList);
        showAccount(indexAccount, forceRefresh, onlyAccount);
    }
}

async function nextAccount(onlyAccount = false) {
    indexAccount = (indexAccount + 1) % accountsList.length;
    await showAccount(indexAccount, true, onlyAccount);
}

async function previousAccount(onlyAccount = false) {
    --indexAccount;
    if (indexAccount < 0) {
        indexAccount = accountsList.length - 1;
    };
    await showAccount(indexAccount, true, onlyAccount);
}

async function nextPost() {

    let accountName = accountsList[indexAccount];
    ++indexPost;

    if(indexPost >= postsListByAccount[accountName].length) {
        indexPost = 0;
        // In case of "Date mode" then we loop on post for all account for a specific date
        if (byDate) {
            indexAccount = (indexAccount + 1) % accountsList.length;
            return await showAccount(indexAccount, true, false, indexPost);
        }
    }

    await showPost(indexAccount, indexPost);
}

async function previousPost() {

    let accountName = accountsList[indexAccount];
    --indexPost;

    if (indexPost < 0) {
        indexPost = postsListByAccount[accountName].length - 1;
        // In case of "Date mode" then we loop on post for all account for a specific date
        if (byDate) {
            --indexAccount;
            if (indexAccount < 0) {
                indexAccount = accountsList.length - 1;
            };
            accountName = accountsList[indexAccount];
            indexPost = postsListByAccount[accountName].length - 1;
            return await showAccount(indexAccount, true, false, indexPost);
        }
    };

    await showPost(indexAccount, indexPost);
}

async function submitPostNumber() {
    let inputPost = parseInt(document.getElementById("post-select-number-input").value)
    let accountName = accountsList[indexAccount];

    if (inputPost > postsListByAccount[accountName].length) {
        indexPost = postsListByAccount[accountName].length - 1
    } else if (inputPost < 1) {
        indexPost = 0;
    } else {
        indexPost = inputPost - 1;
    }
    await showPost(indexAccount, indexPost);
}

async function nextImage() {
    indexImage = (indexImage + 1) % totalImage;
    await showImage(indexAccount, indexPost, indexImage);
}

async function previousImage() {
    --indexImage;
    if (indexImage < 0) {
        indexImage = totalImage - 1;
    };
    await showImage(indexAccount, indexPost, indexImage);
}

function switchDateMode() {
    byDate = !byDate;
    switchElement("date", byDate, ["flex", "none"]);
    if (!byDate) {
        refreshAccount(true);
    }
}

function switchElement(id, check, values) {
    let element = document.getElementById(id);
    element.style.display = check ? values[0] : values[1];
}

async function previousDay() {
    if (updateDateInput(-86400000)) {
        refreshAccount(true);
    }
}

async function nextDay() {
    if (updateDateInput(86400000)) {
        refreshAccount(true);
    }
}

function updateDateInput(delta) {
    let inputDate = document.getElementById("date-information-input");
    if (inputDate.value.length > 0) {
        let date = new Date(inputDate.value);
        date.setMilliseconds(date.getMilliseconds() + delta);
        inputDate.value = date.toISOString().split('T')[0];
        return true;
    }
    return false;
}

async function submitDate() {
    let inputDate = document.getElementById("date-information-input");
    console.log(inputDate.value)
    if (inputDate.value.length > 0) {
        refreshAccount(true);
    }
}