

window.addEventListener("load", function f() {
    chrome.storage.sync.get("uuid", netflixSuggest_onUUID_loaded)
}, false);