// This web UI is made more of less following this tutorial: https://youtu.be/1iysNUrI3lw


const search = document.getElementById('search');
const matchList = document.getElementById('match-list');

// Here we send a request our suggestion engine
const outputSuggestions = async prefix => {
    if (prefix.length === 0) {
        let suggestions = []
        outputHTML(suggestions)
    }
    else {
        let endpoint = 'http://0.0.0.0:18000/get_suggestions/' + prefix;
        let response = await fetch(endpoint);
        if (response.ok) {
            let responseJSON = await response.json();
            let suggestions = responseJSON['result']
            outputHTML(suggestions)
        } else {
            console.log('Fetching error, please consider')
        }
    }
        
}

const outputHTML = suggestions => {
    if(suggestions.length > 0){
        const htlm = suggestions.map(suggestion => 
            `<div class="card card-body">${suggestion}</div>`).join(' ');
    
    matchList.innerHTML = htlm

    }
    else {
        matchList.innerHTML = ''
    }
}

search.addEventListener('input', () => outputSuggestions(search.value));
