"use strict";

const {app, BrowserWindow, Menu} = require('electron');

let win;

function createWindow() {
    win = new BrowserWindow({
        width: 1280,
        height: 720,
        webPreferences: {
            nodeIntegration: true
        }
    });

    //win.setMenu(null);
    //win.setMenuBarVisibility(false);
    win.loadFile('index.html');
}

app.on('ready', createWindow);
app.on('window-all-closed', () => {
    app.quit();
});
