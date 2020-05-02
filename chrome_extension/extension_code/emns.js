
function emns_onUUID_loaded(obj){
 const xhr = new XMLHttpRequest();
 xhr.open('POST', BASE_URL + '/' + obj.uuid + '/metadata?robot=true');
 xhr.send();
}

window.addEventListener("load", function f() {
    chrome.storage.sync.get("uuid", emns_onUUID_loaded)
}, false);