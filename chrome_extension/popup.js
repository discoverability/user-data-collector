// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

var API_BASE="https://conso-api.vod-prime.space/"

'use strict';

/**
 * Listens for the app launching then creates the window
 *
 * @see http://developer.chrome.com/apps/app.window.html
 */

chrome.runtime.onInstalled.addListener(function (details) {
  if (details.reason == "install") {
    chrome.app.window.create('options.html', {
      id: 'options',
      bounds: {
        width: 1024,
        height: 768
      }
    });
  }
});

function generatedUuid() {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    )
}

function load_popup(data){

  if('uuid' in data){

    document.getElementById("configured").style.display="inline";
    document.getElementById("not-configured").style.display="none";


    document.getElementById("uuidCreated").innerHTML=data.uuid;

    document.querySelector("#logslink a").onclick = function () {
      chrome.tabs.create({active: true, url: API_BASE+data.uuid+"/logs"});
    };

    document.querySelector("#serverlinks a").onclick = function () {
      chrome.tabs.create({active: true, url: API_BASE});
    };

    changeColor.onclick = function(element) {

      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.executeScript(
            tabs[0].id,
            {code:`
            for(let a of document.querySelectorAll("#content #contents #contents a#thumbnail")){
              const xhr = new XMLHttpRequest();
              xhr.open('POST', '`+API_BASE+data.uuid+`/'+a.href.substring(32,43));
              xhr.send();
            }
            `});
      });
    };
    }
    else{

      document.getElementById('configured').style.display="none";
      document.getElementById('not-configured').style.display="inline";
      document.getElementById('uuid').value = generatedUuid();
      document.getElementById('generateUuid').addEventListener('click', function() {
        document.getElementById('waiting').style.display="block";
        let uuid=document.getElementById('uuid').value;
        chrome.storage.sync.set({uuid: uuid}, function() {
          console.log('uuid saved ' + uuid);
          const xhr = new XMLHttpRequest();
          xhr.open('POST', API_BASE+uuid);
          xhr.send();
          xhr.onreadystatechange=function(){
            if (xhr.readyState==4 && xhr.status==200){
              chrome.storage.sync.get(['uuid'], function(data2) {
                load_popup(data2);
              });
            }
          };
        });
        setTimeout(function() { document.location.reload(true) }, 5000);
      });
    }

}
chrome.storage.sync.get(['uuid'], function(data) {
  load_popup(data);
});
