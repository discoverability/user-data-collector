function generatedUuid() {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    )
}

chrome.runtime.onInstalled.addListener(function() {
  chrome.storage.sync.set({uuid: generatedUuid()});
  chrome.storage.sync.get("uuid", function (obj) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', BASE_URL+"/"+obj.uuid);
    xhr.send();
  })
  chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
    chrome.declarativeContent.onPageChanged.addRules([{
      conditions: [new chrome.declarativeContent.PageStateMatcher({
        pageUrl: {hostEquals: 'developer.chrome.com'},
      })
      ],
          actions: [new chrome.declarativeContent.ShowPageAction()]
    }]);
  });


  chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
    chrome.declarativeContent.onPageChanged.addRules([{
      conditions: [new chrome.declarativeContent.PageStateMatcher({
        pageUrl: {hostEquals: 'www.youtube.com'},
      })
      ],
          actions: [new chrome.declarativeContent.ShowPageAction()]
    }]);
  });

  chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (changeInfo.url && changeInfo.url.includes('youtube')) {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.storage.sync.get("uuid", function (obj) {
            chrome.tabs.executeScript(
                tabs[0].id,
                {code:`
                for(let a of document.querySelectorAll("#content #contents #contents a#thumbnail")){
                  const xhr = new XMLHttpRequest();
                  xhr.open('POST', `+BASE_URL+`/`+obj.uuid+`/'+a.href.substring(32,43));
                  xhr.send();
                }
              `});
            });
        });
    }
  });

});
