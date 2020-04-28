

window.addEventListener("load", function f()
{
    chrome.storage.sync.get("uuid", function(obj){
        netflixWatch_onUUID_loaded(obj.uuid);
    });
}, false);

