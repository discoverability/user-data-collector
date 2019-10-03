window.addEventListener("load", function f(){

    chrome.storage.sync.get("uuid",function (obj) {
        
    for(let a of document.querySelectorAll("#content #contents #contents a#thumbnail")){
        const xhr = new XMLHttpRequest();
        xhr.open('POST', BASE_URL+"/"+obj.uuid+'/'+a.href.substring(32,43));
        xhr.send();
    }
    });
}, false);