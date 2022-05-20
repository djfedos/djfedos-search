// This web UI is made more of less following this tutorial: https://youtu.be/1iysNUrI3lw

const search = document.getElementById('search');
const matchList = document.getElementById('match-list');
const icon = document.getElementById("icon");

// Here we send a request our suggestion engine
const outputSuggestions = async prefix => {
    prefix = prefix.toLowerCase();
    if (prefix.length === 0) {
        outputHTML([]);
    }
    else {
        let endpoint = 'http://0.0.0.0:18000/get_suggestions/' + prefix;
        let response = await fetch(endpoint);
        if (response.ok) {
            let responseJSON = await response.json();
            let suggestions = responseJSON['result'];
            outputHTML(suggestions);
        } else {
            console.log('Fetching error, please consider');
        }
    }        
}

const outputHTML = suggestions => {
    if(suggestions.length > 0){
        const htlm = suggestions.map((sugg_value, sugg_index) => 
            `<div class="card card-body" tabindex="${sugg_index + 1}">${sugg_value}</div>`).join(' ');
    
    matchList.innerHTML = htlm

    }
    else {
        matchList.innerHTML = ''
    }

    // Add a suggested word to the search box by click on it
    // Thanks to this video: https://youtu.be/QxMBHi_ZiT8
    let allSuggs = matchList.querySelectorAll("div");

    for (let i = 0; i < allSuggs.length; i++) {
        allSuggs[i].setAttribute("onclick", "select(this)");
        allSuggs[i].setAttribute("onmouseover", "this.focus()");
        allSuggs[i].setAttribute("onmouseout", "this.blur()");
        allSuggs[i].setAttribute("onkeypress", "search.focus()");
        allSuggs[i].setAttribute("onfocus", "setFocus(this)");
    }

}

function select(element) {
    let chosenWord = element.textContent;
    search.value = chosenWord;
    outputHTML([]);
    search.focus();
}

function setFocus(element) {
    let chosenWord = element.textContent;
    element.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            search.value = chosenWord;
            outputHTML([]);
            search.focus();
        }
        if (event.key === "Backspace") {
            search.focus();
        }
    });
}


// By click on a zoom icon the script looks for a definition of the word (any user input) in Merriam-Webster dictionary
icon.addEventListener("click", () => {
    let userRequest = 'https://www.merriam-webster.com/dictionary/' + search.value;
    window.open(userRequest, '_blank');
});

// The same thing happens by pressing Enter key in the search bar
// https://www.w3schools.com/howto/howto_js_trigger_button_enter.asp
search.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        icon.click();
        }
    
    });



search.addEventListener('input', () => outputSuggestions(search.value));
